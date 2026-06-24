from agents.resume_JD_analysis_agent_state import Resume_analysis_state
from service.request_schema import Resume_JD_AnalysisStructureOutput
from service.database import get_local_session
from sqlmodel import select
from service.models import primary_llm
from prompts.resume_JD_analysis_prompt import report_prompt
from service.database_schema import Resume_table, Resume_analysis_table

# fetch the resume and it's Analysis 
def fetch_resume(state:Resume_analysis_state):
    try:
        if state.max_failure >= 3:
            return {"status": "MaxRetryExceeded"}

        with get_local_session() as DB:
            # Fetch resume related to the user
            statement_resume = select(Resume_table).where(Resume_table.user_id == state.user_id)
            resume_record = DB.exec(statement_resume).first()
            if not resume_record:
                return {
                    "status": "Failure",
                    "max_failure": state.max_failure + 1
                }
            # Fetch resume analysis related to the resume
            statement_analysis = select(Resume_analysis_table).where(Resume_analysis_table.resume_id == resume_record.id)
            analysis_record = DB.exec(statement_analysis).first()
            if not analysis_record:
                return {
                    "status": "Failure",
                    "max_failure": state.max_failure + 1
                }
            # Store the analysis in state
            resume_analysis_dict = {
                "skills": analysis_record.skills,
                "experience": analysis_record.experience,
                "projects": analysis_record.projects,
                "education": analysis_record.education,
                "summary": analysis_record.summary
            }
            return {
                "resume_analysis": resume_analysis_dict,
                "status": "Success"
            }

    except Exception as e:
        return {
            "status": "Failure",
            "max_failure": state.max_failure + 1
        }
    

#create report

def report_node(state: Resume_analysis_state):
    try:
        if state.max_failure < 3:

            resume_analysis_prompt = report_prompt(state.resume_analysis,state.detaild_JD)
            structured_llm = primary_llm.with_structured_output(
                Resume_JD_AnalysisStructureOutput
            )
            response = structured_llm.invoke(
                resume_analysis_prompt
            )
            return {
                "report": response.model_dump(),
                "status": "Success"
            }
        return {
            "status": "MaxRetryExceeded"
        }
    except Exception:
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

def check_fetch_resume(state: Resume_analysis_state):
    if state.status == "Success":
        return "report"
    if state.status == "MaxRetryExceeded":
        return "end"
    return "fail"