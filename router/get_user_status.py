from fastapi import APIRouter, Depends, status, HTTPException
from service.jwt_token import get_current_user
from service.database_operations import fetch_resume, fetch_interviews, fetch_readmap
import logging

router = APIRouter(prefix="/api")

@router.get("/user_status", tags=["User"])
def get_user_status(user=Depends(get_current_user)):
    try:
        resume = fetch_resume(user["id"])
        interviews = fetch_interviews(user["id"])
        roadmap = fetch_readmap(user["id"])
        
        return {
            "has_resume": resume is not None,
            "total_interviews": len(interviews) if interviews else 0,
            "has_roadmap": roadmap is not None,
            "user_info": {
                "name": user.get("name"),
                "email": user.get("email")
            }
        }
    except Exception as e:
        logging.error("Error getting user status", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
