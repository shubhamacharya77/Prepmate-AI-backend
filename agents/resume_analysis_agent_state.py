from pydantic import BaseModel
from typing import Literal

class Resume_analysis_state(BaseModel):
    user_id:int
    resume_id:int=None
    resume_raw_text:str=""
    Resume_analysis:dict={}
    status:Literal["Success","Failure","MaxRetryExceeded"]| None =None
    max_failure:int=0
