from fastapi import APIRouter,HTTPException,status,Depends,File,UploadFile,BackgroundTasks,Form
from service.supabase_init import uploadResumeSupabase
from service.jwt_token import get_current_user
from service.vectorstore import store_resume_vector
from service.database_operations import uploadResumeDatabase
from agents.resume_analysis_agent import resume_analysis_store_in_DB
from agents.resume_JD_analysis_agent import resume_JD_analysis_store_in_DB
from utils.pdf_txt import extract_resume_text
router= APIRouter(prefix="/api")
    

@router.post("/upload_resume",tags=["Resume"])
async def upload_resume(background_tasks:BackgroundTasks, Desired_Position: str = Form(...),resume: UploadFile = File(...),user=Depends(get_current_user)):
    try:
        #this will extract the raw text from the resume 
        raw_resume_text=await extract_resume_text(resume)

        #this stores the resume in vector DB
        await store_resume_vector(resume,user["id"])

        resume_name = resume.filename

        #the actual file is stored in supabase
        supabase_details = await uploadResumeSupabase(resume,user["id"])

        #this will stores the details of resume in postgresDB
        uploadResumeDatabase(user["id"],resume_name,supabase_details,raw_resume_text)

        # this will invoke the agent and start analysis for the resume 
        background_tasks.add_task(resume_analysis_store_in_DB,user["id"])
        background_tasks.add_task(resume_JD_analysis_store_in_DB,user["id"],Desired_Position)
        return {
            "message": "resume uploaded!"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )