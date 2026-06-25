from fastapi import APIRouter, status, HTTPException, Depends
from service.jwt_token import get_current_user
from service.database_operations import fetch_resume_analysis_by_user

router = APIRouter(prefix="/api")

@router.get("/resume_analysis", tags=["Resume"])
def get_resume_analysis(user=Depends(get_current_user)):
    try:
        analysis = fetch_resume_analysis_by_user(user["id"])
        if analysis:
            return {
                "skills": analysis.skills,
                "experience": analysis.experience,
                "projects": analysis.projects,
                "education": analysis.education,
                "summary": analysis.summary
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No resume analysis found for this user. Please upload a resume first."
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
