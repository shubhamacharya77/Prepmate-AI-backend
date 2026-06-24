from pydantic import BaseModel
from typing import Literal

class Resume_analysis_state(BaseModel):
    user_id:int
    detaild_JD:str
    resume_analysis:dict={}
    report:dict
    status:Literal["Success","Failure","MaxRetryExceeded"]| None =None
    max_failure:int=0
    
