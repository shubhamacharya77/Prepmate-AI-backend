from supabase import create_client
from fastapi import HTTPException,status,UploadFile
from dotenv import load_dotenv
load_dotenv()
import os
import logging

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

async def uploadResumeSupabase(resume:UploadFile,user_id:int):

    try:
        filename = resume.filename.replace(" ", "_")
        path = f"{user_id}/{filename}"

        await resume.seek(0)
        content = await resume.read()
        response=supabase.storage.from_("resume").upload(
        path=path,
        file=content,
        file_options={
        "content-type": resume.content_type
    })
        return {"storage":response }
    except Exception as e:
        logging.error("Error uploading to Supabase", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


def delete_resume_supabase(path: str):
    try:
        response = supabase.storage.from_("resume").remove([path])
        return {"delete_response": response}
    except Exception as e:
        logging.error("Error deleting from Supabase", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )