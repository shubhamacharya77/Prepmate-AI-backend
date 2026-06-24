from fastapi import APIRouter,status,HTTPException,Depends
from agents.career_roadmap_agent import generate_career_roadmap
from service.jwt_token import get_current_user
from service.database_operations import fetch_readmap,fetch_resume

router = APIRouter(prefix="/api")

@router.get("/road_map", tags=["road_map"])
def road_map(user=Depends(get_current_user)):
    try:
        road_map_data=fetch_readmap(user["id"])
        if road_map_data:
            return road_map_data
        else:
            resume=fetch_resume(user["id"])
            if not resume:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No resume found for this user. Please upload a resume first."
                )
            generated = generate_career_roadmap(user["id"],resume.id)
            return generated
    except HTTPException:
        raise
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))