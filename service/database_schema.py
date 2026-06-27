from sqlmodel import SQLModel,Field,Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import EmailStr
from datetime import datetime,timezone
from typing import Optional
#user 
class User_table(SQLModel,table=True):
    id:int=Field(default=None,primary_key=True)
    name:str=Field(index=True)
    email:EmailStr=Field(index=True,unique=True)
    resume:Optional["Resume_table"]=Relationship(back_populates="user")
    resumeJDAnalysis:Optional["ResumeJDAnalysis_table"]=Relationship(back_populates="user")
    career_roadmap: Optional["Career_Roadmap_table"] = Relationship(back_populates="user")
    interviews:list["Interviews_table"]=Relationship(back_populates="user")

#resume 
class Resume_table(SQLModel,table=True):
    id:int=Field(default=None,primary_key=True)
    user_id:int=Field(index=True,foreign_key="user_table.id",unique=True)
    resume_name:str=Field(index=True)
    resume_raw_txt:str=Field(default=None)
    resume_path:str=Field(default=None)
    user:Optional["User_table"]=Relationship(back_populates="resume")
    resume_analysis:Optional["Resume_analysis_table"]=Relationship(back_populates="resume")
    career_roadmap: Optional["Career_Roadmap_table"] = Relationship(back_populates="resume")

# what skills user have 
class Resume_analysis_table(SQLModel,table=True):
    id:int=Field(default=None,primary_key=True)
    resume_id:int=Field(index=True,foreign_key="resume_table.id",unique=True)
    skills:list=Field(sa_column=Column(JSONB))
    experience:list = Field(sa_column=Column(JSONB))
    projects:list = Field(sa_column=Column(JSONB))
    education:list = Field(sa_column=Column(JSONB))
    summary:str=Field(default=None)
    resume:Optional["Resume_table"]=Relationship(back_populates="resume_analysis")


# resume v/s JD analysis
class ResumeJDAnalysis_table(SQLModel, table=True):
    id:int= Field(default=None, primary_key=True)
    resume_id: int = Field(index=True,foreign_key="resume_table.id",unique=True)
    user_id:int=Field(index=True,foreign_key="user_table.id",unique=True)
    match_score: float = Field(default=0.0,le=100,ge=0)
    matched_skills: list[str] = Field(default_factory=list,sa_column=Column(JSONB))
    missing_skills: list[str] = Field(default_factory=list,sa_column=Column(JSONB) )
    additional_skills: list[str] = Field( default_factory=list,sa_column=Column(JSONB))
    experience_match: bool = Field(default=False)
    required_experience: str = Field(default="")
    candidate_experience: str = Field(default="")
    experience_gap: str = Field(default="")
    relevant_projects: list[str] = Field(default_factory=list, sa_column=Column(JSONB))
    missing_project_domains: list[str] = Field( default_factory=list, sa_column=Column(JSONB))
    strengths: list[str] = Field( default_factory=list,  sa_column=Column(JSONB))
    weaknesses: list[str] = Field( default_factory=list,  sa_column=Column(JSONB))
    recommendations: list[str] = Field(default_factory=list,   sa_column=Column(JSONB) )
    ats_keywords_found: list[str] = Field(default_factory=list,sa_column=Column(JSONB))
    ats_keywords_missing: list[str] = Field( default_factory=list, sa_column=Column(JSONB))
    summary: str = Field(default="")
    user:Optional["User_table"]=Relationship(back_populates="resumeJDAnalysis")


# Career Roadmap
class Career_Roadmap_table(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    resume_id: int = Field(index=True, foreign_key="resume_table.id",unique=True)
    user_id: int = Field(index=True, foreign_key="user_table.id",unique=True)
    goal: str = Field(default="")
    roadmap: dict = Field(default_factory=dict, sa_column=Column(JSONB))
    user: Optional["User_table"] = Relationship(back_populates="career_roadmap")
    resume: Optional["Resume_table"] = Relationship(back_populates="career_roadmap")

##### Interview-Prepmate ##########

class Interviews_table(SQLModel,table=True):
    id: int =Field(default=None,primary_key=True)
    user_id: int=Field(foreign_key="user_table.id")
    title:str=Field(default=None)
    difficulty_level:str=Field( default=None)
    interviews_type:str = Field(default=None)
    status:str=Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user:Optional["User_table"]=Relationship(back_populates="interviews")
    question_answer:list["QandA"]=Relationship(back_populates="interview")
    report:Optional["final_interview_report"]=Relationship(back_populates="interview")

class QandA(SQLModel,table=True):
    id: int =Field(default=None,primary_key=True)
    interview_id:int=Field(foreign_key="interviews_table.id")
    interview_type:str= Field(default=None)
    question: list = Field( default_factory=list,sa_column=Column(JSONB))
    answer: list = Field(default_factory=list,sa_column=Column(JSONB))
    created_at:datetime = Field( default_factory=lambda: datetime.now(timezone.utc))
    interview:Optional["Interviews_table"]=Relationship(back_populates="question_answer")

class final_interview_report(SQLModel,table=True):
    id:int =Field(default=None,primary_key=True)
    interview_id: int=Field(foreign_key="interviews_table.id",unique=True)
    strengths:str=Field(default=None)
    weaknesses:str=Field(default=None)
    final_feedback:str=Field(default=None)
    final_score: int = Field(default=0, ge=0,le=100)
    interview:Optional["Interviews_table"]=Relationship(back_populates="report")