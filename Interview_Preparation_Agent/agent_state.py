from pydantic import BaseModel
from typing import Literal
from service.request_schema import Q_and_A_store_schema
class agnetstate(BaseModel):
    user_id:int
    interview_id:int
    title:str
    status:Literal["Start","Complete"]
    interview_type:Literal["Technical","Hr"]
    difficulty_level:Literal["Hard","Medium","Easy"]
    resume_context:dict|None =None
    generated_questions:list[dict]|None= None
    count:int=0
    Q_and_A:Q_and_A_store_schema|None=None
    report:dict={}
    