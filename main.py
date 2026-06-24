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
from router.post_question_answer import router as post_interview_question
# from test import router as test
from sqlmodel import SQLModel
from service.database import engine
from Interview_Preparation_Agent.agent import checkpointer
from dotenv import load_dotenv
from service.database_schema import *
import os
load_dotenv()

app = FastAPI(title="PrepMate")
frontend_origins = list(
    dict.fromkeys(
        [
            os.getenv("FRONTEND_URL", "http://localhost:5173"),
            os.getenv("ALLOWED_ORIGIN", "http://localhost:3000"),
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
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
app.include_router(job_search)
app.include_router(road_map)
app.include_router(create_interview)
app.include_router(start_interview)
app.include_router(post_interview_question)
# app.include_router(test)
@app.get("/",status_code=status.HTTP_200_OK)
def healthCheck():
    return{
        "message":"server is running !"
    }