from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from router.Oauth_callback import router as login_router
from router.Oauth import router as Oauth_router
from router.user_delete import router as user_delete
from router.resume_upload import router as resume_upload
from router.resume_delete import router as resume_delete
from router.job_search import router as job_search
from router.road_map import router as road_map
from router.create_interview import router as create_interview
from router.get_interview_question import router as start_interview
from router.send_answer import router as post_interview_question
from router.get_resume_analysis import router as get_resume_analysis_router
from router.get_interview_history import router as get_interview_history_router
from router.get_interview_details import router as get_interview_details_router
from router.get_user_status import router as get_user_status_router
from sqlmodel import SQLModel
from service.database import engine
from Interview_Preparation_Agent.agent import checkpointer
from service.database_schema import *
from dotenv import load_dotenv
import os
import logging
load_dotenv()

# Configure global logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
app = FastAPI(title="PrepMate")
frontend_origins = list(
    dict.fromkeys(
        [
            os.getenv("FRONTEND_URL", "https://prepmate-ai-frontend.vercel.app"),
        ]
    )
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

checkpointer.setup()
SQLModel.metadata.create_all(engine)

app.include_router(login_router)
app.include_router(Oauth_router)
app.include_router(user_delete)
app.include_router(resume_upload)
app.include_router(resume_delete)
app.include_router(get_resume_analysis_router)
app.include_router(get_interview_history_router)
app.include_router(get_interview_details_router)
app.include_router(job_search)
app.include_router(road_map)
app.include_router(create_interview)
app.include_router(start_interview)
app.include_router(post_interview_question)
app.include_router(get_user_status_router)

@app.get("/",status_code=status.HTTP_200_OK)
def healthCheck():
    return{
        "message":"server is running !"
    }