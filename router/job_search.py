from fastapi import APIRouter,status,HTTPException,Depends
from agents.Job_search_agent import Job_analysis
from service.jwt_token import get_current_user
router = APIRouter(prefix="/api")

@router.post("/job_search", tags=["job_search"])
def job_search(JD:str,user=Depends(get_current_user)):
    try:
        response=Job_analysis(user["id"],JD)
        return response
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))