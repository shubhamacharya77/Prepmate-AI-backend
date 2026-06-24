from fastapi import APIRouter,status,HTTPException,Depends
from service.jwt_token import get_current_user
from service.database_operations import fetch_active_interview
from Interview_Preparation_Agent.agent import copilot_workflow
from langgraph.types import Command
router = APIRouter(prefix="/api")
@router.post("/get_interview_questions", tags=["Interview"])
def start_interview(user=Depends(get_current_user)):
    try:
        interview=fetch_active_interview(user["id"])
        if not interview:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active interview found for this user. Please create one first."
            )
        config={
            "configurable":{
                "user_id":user["id"],
                "thread_id":interview.id
            }
        }
        state_snapshot = copilot_workflow.get_state(config)
        
        if state_snapshot.tasks and state_snapshot.tasks[0].interrupts:
            interrupt_val = state_snapshot.tasks[0].interrupts[0].value
            if "message" in interrupt_val and interrupt_val["message"] == "waiting... for user input...":
                # We are at the very beginning. Resume the graph so it generates the first question.
                copilot_workflow.invoke(Command(resume="start"), config=config)
                # Refresh state snapshot to get the new interrupt (which should be the first question)
                state_snapshot = copilot_workflow.get_state(config)
                if state_snapshot.tasks and state_snapshot.tasks[0].interrupts:
                    interrupt_val = state_snapshot.tasks[0].interrupts[0].value
                    return {"question": interrupt_val.get("question")}
            
            elif "question" in interrupt_val:
                # We are already at a question interrupt. Just return the question.
                return {"question": interrupt_val.get("question")}
        
        return {"question": None, "status": "Interview Completed or Error"}
    except HTTPException:
        raise
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
