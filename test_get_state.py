import os
from psycopg import Connection
with open(".env") as f:
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            os.environ[k] = v.strip("'\"")
db_url = os.environ.get("DATABASE_URL", "")
if "+psycopg" in db_url:
    db_url = db_url.replace("+psycopg", "")

from langgraph.checkpoint.postgres import PostgresSaver
conn = Connection.connect(db_url, autocommit=True)
checkpointer = PostgresSaver(conn)

from Interview_Preparation_Agent.agent import copilot_workflow
copilot_workflow.checkpointer = checkpointer

from service.database import SessionLocal
from service.database_schema import Interviews_table

db = SessionLocal()
# Get the most recent active interview
interview = db.query(Interviews_table).order_by(Interviews_table.id.desc()).first()

print(f"Testing state for interview_id: {interview.id}, user_id: {interview.user_id}")

config = {
    "configurable": {
        "user_id": interview.user_id,
        "thread_id": str(interview.id)
    }
}

try:
    state = copilot_workflow.get_state(config)
    print("State tasks:", state.tasks)
except Exception as e:
    import traceback
    traceback.print_exc()

