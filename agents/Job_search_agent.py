from langgraph.graph import StateGraph,START,END
from agents.Job_search_agent_state import JD_analysis_state
from agents.Job_search_agent_node import *


graph=StateGraph(JD_analysis_state)

graph.add_node("analysis_node",analysis_node)
graph.add_node("fetch_jobs",Job_search)

graph.add_edge(START,"analysis_node")
graph.add_edge("analysis_node","fetch_jobs")
graph.add_conditional_edges("fetch_jobs",status_check,{"end":END,"fail":"analysis_node"})

#graph compiling 
analysis_workflow=graph.compile()


def Job_analysis(user_id:int,JD:str):
    try:
        print("Background task started")
        analysis=analysis_workflow.invoke({
            "user_id":user_id,
            "detaild_JD":JD
        })
        jobs=analysis["Job_search"]
        print("Task complted")
        return jobs
    except Exception as e :
        raise Exception(str(e))

