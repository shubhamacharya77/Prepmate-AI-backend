from langgraph.graph import StateGraph, START, END
from agents.career_roadmap_agent_state import CareerRoadmapState
from agents.career_roadmap_agent_node import *

graph = StateGraph(CareerRoadmapState)

# graph nodes
graph.add_node("fetch_analysis", fetch_analysis)
graph.add_node("generate_roadmap", generate_roadmap_node)
graph.add_node("save_roadmap", save_roadmap_to_db)

# edges
graph.add_edge(START, "fetch_analysis")
graph.add_conditional_edges("fetch_analysis", check_fetch_analysis, {"generate_roadmap": "generate_roadmap", "fail": "fetch_analysis", "end": END})
graph.add_conditional_edges("generate_roadmap", check_generate_roadmap, {"save_roadmap": "save_roadmap", "fail": "generate_roadmap", "end": END})
graph.add_conditional_edges("save_roadmap", status_check, {"end": END, "fail": "save_roadmap"})

# graph compiling
roadmap_workflow = graph.compile()

def generate_career_roadmap(user_id: int, resume_id: int):
    try:
        print("Career Roadmap Generation started")
        
        # Invoke workflow
        state_output = roadmap_workflow.invoke({
            "user_id": user_id,
            "resume_id": resume_id
        })
        
        print("Workflow Output Status:", state_output.get("status"))
        
        if state_output.get("status") != "Success":
            raise Exception(f"Roadmap workflow failed. Final status: {state_output.get('status')}")
            
        return state_output.get("roadmap")
    except Exception as e:
        raise Exception(f"Failed to generate roadmap: {str(e)}")
