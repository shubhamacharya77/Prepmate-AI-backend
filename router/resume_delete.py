from fastapi import APIRouter,HTTPException,status,Depends
from service.database import get_session,Session
from service.database_schema import Resume_table,Resume_analysis_table
from sqlmodel import select
from service.supabase_init import delete_resume_supabase
from service.vectorstore import delete_resume_vector
from service.jwt_token import get_current_user
from service.database_operations import deleteResumeDatabase
import logging

router= APIRouter(prefix="/api")

@router.delete("/delete_resume",tags=["Resume"])
def upload_delete(user=Depends(get_current_user),db: Session = Depends(get_session)):
    try:
        #find the resume
        resume=db.exec(select(Resume_table).where(Resume_table.user_id==user["id"])).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No resume found for this user."
            )
        
        # delete from supabase
        delete_resume_supabase(resume.resume_path)

        # delete from vector store
        delete_resume_vector(resume.user_id)
        
        #delete analysis and the resume as well from database
        deleteResumeDatabase(resume)
        return {
            "message": "resume deleted!",
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error("Error deleting resume", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )