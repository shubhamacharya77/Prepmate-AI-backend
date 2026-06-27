from agents.resume_analysis_agent_state import Resume_analysis_state
from utils.get_resume_txt_DB import get_raw_resume_txt_from_DB
from service.request_schema import ResumeAnalysisStructureOutput
from prompts.resume_analysis import analysis_prompt
from service.models import primary_llm
import logging



def get_resume(state:Resume_analysis_state):
    try:
        user_id=state.user_id
        resume=get_raw_resume_txt_from_DB(user_id)
        return{
            "resume_id":resume["id"],
            "resume_raw_text":resume["text"]
        }
    except Exception as e:
        logging.error("Failed to get resume from DB", exc_info=True)
        raise

def analysis_node(state: Resume_analysis_state):
    try:
        if state.max_failure < 3:

            resume_analysis_prompt = analysis_prompt(
                state.resume_raw_text
            )

            structured_llm = primary_llm.with_structured_output(
                ResumeAnalysisStructureOutput
            )

            response = structured_llm.invoke(
                resume_analysis_prompt
            )

            return {
                "Resume_analysis": response.model_dump(),
                "status": "Success"
            }

        return {
            "status": "MaxRetryExceeded"
        }

    except Exception as e:
        logging.error("Error in analysis_node", exc_info=True)
        return {
            "status": "Failure",
            "max_failure": state.max_failure + 1
        }

#conditinal method
def status_check(state: Resume_analysis_state):
    if state.status == "Success":
        return "end"

    if state.status == "MaxRetryExceeded":
        return "end"

    return "fail"