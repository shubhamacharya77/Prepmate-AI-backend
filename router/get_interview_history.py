from fastapi import APIRouter, status, HTTPException, Depends
from service.jwt_token import get_current_user
from service.database_operations import fetch_interviews
import logging

router = APIRouter(prefix="/api")

@router.get("/get_interviews", tags=["Interview"])
def get_interview_history(user=Depends(get_current_user)):
    try:
        interviews = fetch_interviews(user["id"])
        if interviews:
            # Format the output for the UI
            history = []
            for interview in interviews:
                history.append({
                    "id": interview.id,
                    "title": interview.title,
                    "difficulty_level": interview.difficulty_level,
                    "interviews_type": interview.interviews_type,
                    "status": interview.status,
                    "created_at": interview.created_at
                })
            return {"history": history}
        else:
            return {"history": []}
    except Exception as e:
        logging.error("Error getting interview history", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
