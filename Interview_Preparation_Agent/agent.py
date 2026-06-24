from langgraph.graph import StateGraph,START,END
from Interview_Preparation_Agent.agent_state import agnetstate
from Interview_Preparation_Agent.agent_node import *
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg import Connection
from dotenv import load_dotenv
import os
load_dotenv()

db_url = os.getenv("DATABASE_URL", "")
if "+psycopg" in db_url:
    db_url = db_url.replace("+psycopg", "")

conn = Connection.connect(db_url, autocommit=True)
checkpointer = PostgresSaver(conn)

graph=StateGraph(agnetstate)

graph.add_node("fetch_context",fetch_context)
graph.add_node("generate_questions",generate_questions)
graph.add_node("interrupt_node",interrupt_node)
graph.add_node("get_question",get_question)
graph.add_node("store_answer",store_answer),
graph.add_node("report_node",report_node)

graph.add_edge(START,"fetch_context")
graph.add_edge("fetch_context","generate_questions")
graph.add_edge("generate_questions","interrupt_node")
graph.add_conditional_edges("interrupt_node",checknode,{"report_node":"report_node","question_node":"get_question"})
graph.add_edge("get_question","store_answer")
graph.add_conditional_edges("store_answer",checknode,{"report_node":"report_node","question_node":"get_question"})
graph.add_edge("report_node",END)

#invoke with config....
copilot_workflow=graph.compile(checkpointer=checkpointer)
