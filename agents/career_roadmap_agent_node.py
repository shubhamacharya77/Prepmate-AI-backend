from agents.career_roadmap_agent_state import CareerRoadmapState
from service.request_schema import CareerRoadmapStructureOutput
from service.database import get_local_session
from sqlmodel import select
from service.models import primary_llm
from prompts.career_roadmap_prompt import get_roadmap_prompt
from service.database_schema import ResumeJDAnalysis_table
from service.database_operations import store_road_map
import logging

def fetch_analysis(state: CareerRoadmapState):
    try:
        if state.max_failure >= 3:
            return {"status": "MaxRetryExceeded"}

        with get_local_session() as DB:
            # Fetch the resume vs JD analysis report
            analysis_record = DB.exec(select(ResumeJDAnalysis_table).where((ResumeJDAnalysis_table.user_id == state.user_id) & (ResumeJDAnalysis_table.resume_id == state.resume_id))).first()
            if not analysis_record:
                return {
                    "status": "Failure",
                    "max_failure": state.max_failure + 1
                }   
            # Serialize the needed fields to pass to the prompt
            analysis_dict = {
                "match_score": analysis_record.match_score,
                "matched_skills": analysis_record.matched_skills,
                "missing_skills": analysis_record.missing_skills,
                "experience_gap": analysis_record.experience_gap,
                "strengths": analysis_record.strengths,
                "weaknesses": analysis_record.weaknesses,
                "recommendations": analysis_record.recommendations,
                "summary": analysis_record.summary
            }
            
            return {
                "resume_jd_analysis": analysis_dict,
                "status": "Success"
            }

    except Exception as e:
        logging.error(f"Error in fetch_analysis: {e}")
        return {
            "status": "Failure",
            "max_failure": state.max_failure + 1
        }
        

def generate_roadmap_node(state: CareerRoadmapState):
    try:
        if state.max_failure < 3:
            roadmap_prompt = get_roadmap_prompt(state.resume_jd_analysis)
            structured_llm = primary_llm.with_structured_output(CareerRoadmapStructureOutput)
            
            response = structured_llm.invoke(roadmap_prompt)
            return {
                "roadmap": response.model_dump(),
                "status": "Success"
            }
        return {
            "status": "MaxRetryExceeded"
        }
    except Exception as e:
        return {
            "status": "Failure",
            "max_failure": state.max_failure + 1
        }


def save_roadmap_to_db(state: CareerRoadmapState):
    try:
        if state.max_failure < 3:
            data={
            "resume_id":state.resume_id,
            "user_id":state.user_id,
            "goal":state.roadmap.get("goal"),
            "roadmap":state.roadmap
            }
            store_road_map(data)
            
            return {
                "status": "Success"
            }
        return {
            "status": "MaxRetryExceeded"
        }
    except Exception as e:
        return {
            "status": "Failure",
            "max_failure": state.max_failure + 1
        }


def status_check(state: CareerRoadmapState):
    if state.status == "Success":
        return "end"

    if state.status == "MaxRetryExceeded":
        return "end"

    return "fail"

def check_fetch_analysis(state: CareerRoadmapState):
    if state.status == "Success":
        return "generate_roadmap"
    if state.status == "MaxRetryExceeded":
        return "end"
    return "fail"

def check_generate_roadmap(state: CareerRoadmapState):
    if state.status == "Success":
        return "save_roadmap"
    if state.status == "MaxRetryExceeded":
        return "end"
    return "fail"
