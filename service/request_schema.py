from pydantic import BaseModel,Field
from typing import Optional,List,Literal
#JWT schemas 
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: List[str] = []

#Resume Analysis structure output

class Resume_analysis_structure_output(BaseModel):
    personal_info:dict
    Skills:List
    experience:List | None=None
    project_details:List | None=None
    education_details:List
    achievements:List | None=None
    resume_detailed_summary:str
class Experience(BaseModel):
    company: str
    role: str
    duration: Optional[str] = None
    description: Optional[List[str]] = None
    technologies: Optional[List[str]] = None


class Project(BaseModel):
    project_name: str
    description: str
    technologies: List[str]
    github_link: Optional[str] = None


class Education(BaseModel):
    institution: str
    degree: str
    graduation_year: Optional[str] = None
    cgpa: Optional[str] = None


class ResumeAnalysisStructureOutput(BaseModel):
    personal_info: dict
    skills: List[str]
    experience: Optional[List[Experience]] = None
    project_details: Optional[List[Project]] = None
    education_details: List[Education]
    achievements: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    resume_detailed_summary: str


# JD analysis structure output 
class JDAnalysisStructureOutput(BaseModel):
    job_title: Optional[str] = None
    required_skills: List[str] = []


class Resume_JD_AnalysisStructureOutput(BaseModel):
    match_score: float = 0.0
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    additional_skills: list[str] = Field(default_factory=list)
    experience_match: bool = False
    required_experience: str = ""
    candidate_experience: str = ""
    experience_gap: str = ""
    relevant_projects: list[str] = Field(default_factory=list)
    missing_project_domains: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    ats_keywords_found: list[str] = Field(default_factory=list)
    ats_keywords_missing: list[str] = Field(default_factory=list)
    summary: str = ""


# Career Roadmap structured output
class RoadmapTopic(BaseModel):
    month: str = Field(description="The month or phase identifier, e.g., 'Month 1'")
    topics: str = Field(description="The core topics to cover during this month, e.g., 'Python + ML'")
    details: str = Field(description="Detailed explanation of what to study and why it's important for the goal")

class CareerRoadmapStructureOutput(BaseModel):
    goal: str = Field(description="The inferred or provided goal for this roadmap")
    roadmap: List[RoadmapTopic] = Field(description="A month-by-month career roadmap to achieve the goal")


class Interview_details_schema(BaseModel):
    topic:str
    difficulty_level:Literal["Hard","Medium","Easy"] 
    interview_type:Literal["Technical","Hr"]
    status:Literal["Start","Complete"]
    
class Q_generation_schema(BaseModel):
    question_no:int
    question:str 
    type:Literal["Technical","Hr"]
    difficulty:Literal["Hard","Medium","Easy"] 

class QListSchema(BaseModel):
    questions: List[Q_generation_schema]

class Q_and_A_store_schema(BaseModel):
    interview_id:int
    question:str
    answer:str
    interview_type:str

class FinalInterviewReportSchema(BaseModel):
    strengths: str = Field(description="Candidate's key strengths")
    weaknesses: str = Field( description="Candidate's key weaknesses")
    final_feedback: str = Field( description="Detailed overall interview feedback")
    final_score: int = Field( ge=0,le=100,description="Overall interview score")

class UserAnswerSchema(BaseModel):
    answer: str