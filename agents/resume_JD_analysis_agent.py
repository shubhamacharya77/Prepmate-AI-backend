from langgraph.graph import StateGraph,START,END
from service.database import get_local_session
from service.database_operations import store_resume_report
from agents.resume_JD_analysis_agent_state import Resume_analysis_state
from agents.resume_JD_analysis_agent_node import *
from sqlmodel import select
from service.database_schema import Resume_table


graph=StateGraph(Resume_analysis_state)

# graphs node
graph.add_node("fetch_resume",fetch_resume)
graph.add_node("report",report_node)


#edges
graph.add_edge(START,"fetch_resume")
graph.add_conditional_edges("fetch_resume", check_fetch_resume, {"report": "report", "fail": "fetch_resume", "end": END})
graph.add_conditional_edges("report",status_check,{"end": END, "fail": "report"})

#graph compiling 

analysis_workflow=graph.compile()


def resume_JD_analysis_store_in_DB(user_id:int, JD:str):
    try:
        print("Background task started")
        # Ensure we pass the required state keys (report defaults to {})
        analysis=analysis_workflow.invoke({"user_id":user_id, "detaild_JD":JD, "report":{}})
        
        print("Workflow Output:")
        
        if analysis.get("status") != "Success":
            raise Exception(f"Workflow failed to complete successfully. Final status: {analysis.get('status')}")
            
        report_data = analysis.get("report", {})
        
        with get_local_session() as DB:
            # We need to get the resume_id for this user
            statement = select(Resume_table).where(Resume_table.user_id == user_id)
            resume_record = DB.exec(statement).first()
            if not resume_record:
                raise Exception("Resume not found for user")
            data={
                "resume_id":resume_record.id,
                "user_id":user_id,
                "match_score":report_data.get("match_score", 0.0),
                "matched_skills":report_data.get("matched_skills", []),
                "missing_skills":report_data.get("missing_skills", []),
                "additional_skills":report_data.get("additional_skills", []),
                "experience_match":report_data.get("experience_match", False),
                "required_experience":report_data.get("required_experience", ""),
                "candidate_experience":report_data.get("candidate_experience", ""),
                "experience_gap":report_data.get("experience_gap", ""),
                "relevant_projects":report_data.get("relevant_projects", []),
                "missing_project_domains":report_data.get("missing_project_domains", []),
                "strengths":report_data.get("strengths", []),
                "weaknesses":report_data.get("weaknesses", []),
                "recommendations":report_data.get("recommendations", []),
                "ats_keywords_found":report_data.get("ats_keywords_found", []),
                "ats_keywords_missing":report_data.get("ats_keywords_missing", []),
                "summary":report_data.get("summary", "")
            }
            store_resume_report(data)
        print("Task complted")
        return data
    except Exception as e :
        raise Exception(str(e))
