from pydantic import BaseModel
from typing import Literal

class JD_analysis_state(BaseModel):
    user_id:int
    detaild_JD:str
    JD_analysis:dict={}
    Job_search:list=[]
    status:Literal["Success","Failure","MaxRetryExceeded"]| None =None
    max_failure:int=0
