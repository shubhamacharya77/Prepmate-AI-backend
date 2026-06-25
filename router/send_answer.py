from fastapi import APIRouter,status,HTTPException,Depends
from service.jwt_token import get_current_user
from service.database_operations import fetch_active_interview
from Interview_Preparation_Agent.agent import copilot_workflow
from service.request_schema import UserAnswerSchema
from langgraph.types import Command

router = APIRouter(prefix="/api")
@router.post("/post_answer", tags=["Interview"])
def post_answer(answer_payload: UserAnswerSchema, user=Depends(get_current_user)):
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
                "thread_id":str(interview.id)
            }
        }
        copilot_workflow.invoke(Command(resume={"answer": answer_payload.answer}), config=config)
        return {"message": "answer submitted"}
    except HTTPException:
        raise
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))