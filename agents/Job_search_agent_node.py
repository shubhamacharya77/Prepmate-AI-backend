from agents.Job_search_agent_state import JD_analysis_state
from service.request_schema import JDAnalysisStructureOutput
from prompts.JD_analysis import analysis_prompt
from utils.fetch_jobs import fetch_jobs
from service.models import primary_llm

# this will analysis the JD
def analysis_node(state:JD_analysis_state):
    try:
        if state.max_failure < 3:
            JD_analysis_prompt = analysis_prompt(
                state.detaild_JD
            )
            structured_llm = primary_llm.with_structured_output(JDAnalysisStructureOutput)
            response = structured_llm.invoke(
                JD_analysis_prompt
            )
            return {
                "JD_analysis": response.model_dump(),
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

# this will fetch the jobs from adzuna

def Job_search(state:JD_analysis_state):
    try:
        if state.max_failure < 3:
            job_query=f"{state.JD_analysis['job_title']}"
            Jobs=fetch_jobs(job_query)
            return{
             "Job_search":[job.model_dump() for job in Jobs],
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
def status_check(state: JD_analysis_state):
    if state.status == "Success":
        return "end"

    if state.status == "MaxRetryExceeded":
        return "end"

    return "fail"