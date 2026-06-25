from fastapi import APIRouter,status,HTTPException,Depends
from service.jwt_token import get_current_user
from service.request_schema import Interview_details_schema
from service.database_operations import create_interview_in_db, fetch_active_interview
from Interview_Preparation_Agent.agent import copilot_workflow

router = APIRouter(prefix="/api")

@router.post("/create_interview", tags=["Interview"])
def create_interview(interview_details:Interview_details_schema,user=Depends(get_current_user)):
    try:
        # Check if user already has an active interview
        active_interview = fetch_active_interview(user["id"])
        if active_interview:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An interview is already in progress. Please complete or delete it before creating a new one."
            )

        data={
            "id":user["id"],
            "title":interview_details.topic,
            "difficulty_level":interview_details.difficulty_level,
            "interviews_type":interview_details.interview_type,
            "status":interview_details.status
        }
        interview_id=create_interview_in_db(data)
        config={
            "configurable":{
        "user_id":user["id"],
        "thread_id":str(interview_id)
        }
        }
        copilot_workflow.invoke({
        "user_id":data["id"],
        "interview_id":interview_id,
        "title":data["title"],
        "status":data["status"],
        "interview_type":data["interviews_type"],
        "difficulty_level":data["difficulty_level"]
        },config=config)
        return{
            "message":"interview created",
            "interview_id": interview_id
        }
    except HTTPException:
        raise