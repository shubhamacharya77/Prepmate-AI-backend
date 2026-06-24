from pydantic import BaseModel
from typing import Literal

class CareerRoadmapState(BaseModel):
    user_id: int
    resume_id: int
    resume_jd_analysis: dict = {}
    roadmap: dict = {}
    status: Literal["Success", "Failure", "MaxRetryExceeded"] | None = None
    max_failure: int = 0
