from langgraph.graph import StateGraph,START,END
from agents.Job_search_agent_state import JD_analysis_state
from agents.Job_search_agent_node import *
import logging

graph=StateGraph(JD_analysis_state)

graph.add_node("analysis_node",analysis_node)
graph.add_node("fetch_jobs",Job_search)

graph.add_edge(START,"analysis_node")
graph.add_conditional_edges("analysis_node", check_analysis_node, {"fetch_jobs": "fetch_jobs", "fail": "analysis_node", "end": END})
graph.add_conditional_edges("fetch_jobs",status_check,{"end":END,"fail":"analysis_node"})

#graph compiling 
analysis_workflow=graph.compile()


def Job_analysis(user_id:int,JD:str):
    try:
        logging.info("Background task started for Job search")
        analysis=analysis_workflow.invoke({
            "user_id":user_id,
            "detaild_JD":JD
        })
        jobs=analysis.get("Job_search", [])
        logging.info("Job search task completed")
        return jobs
    except Exception as e:
        logging.error("Failed in Job_analysis", exc_info=True)
        raise Exception(f"Job_analysis failed: {str(e)}") from e

