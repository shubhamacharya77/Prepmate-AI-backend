from langgraph.graph import StateGraph,START,END
from agents.resume_analysis_agent_state import Resume_analysis_state
from agents.resume_analysis_agent_node import *
from service.database_operations import store_resume_analysis
from sqlmodel import select
import logging

graph=StateGraph(Resume_analysis_state)

# graphs node
graph.add_node("get_resume",get_resume)
graph.add_node("analysis_node",analysis_node)

#edges

graph.add_edge(START,"get_resume")
graph.add_edge("get_resume","analysis_node")
graph.add_conditional_edges("analysis_node",status_check,{"end":END,"fail":"analysis_node"})

#graph compiling 

analysis_workflow=graph.compile()


def resume_analysis_store_in_DB(user_id:int):
    try:
        logging.info("Resume analysis background task started")
        analysis=analysis_workflow.invoke({"user_id":user_id})
        
        if analysis.get("status") != "Success":
            raise Exception(f"Resume analysis workflow failed. Status: {analysis.get('status')}")
            
        data={
                "resume_id":analysis["resume_id"],
                "skills":analysis["Resume_analysis"]["skills"],
                "experience":analysis["Resume_analysis"]["experience"],
                "projects":analysis["Resume_analysis"]["project_details"],
                "education":analysis["Resume_analysis"]["education_details"],
                "summary":analysis["Resume_analysis"]["resume_detailed_summary"]
        }
        store_resume_analysis(data)
        logging.info("Resume analysis task completed")
    except Exception as e:
        logging.error("Failed in resume_analysis_store_in_DB", exc_info=True)
        raise Exception(f"resume_analysis_store_in_DB failed: {str(e)}") from e
