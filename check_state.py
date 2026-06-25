import sys, os
from psycopg import Connection
from langgraph.checkpoint.postgres import PostgresSaver
from Interview_Preparation_Agent.agent import copilot_workflow
import psycopg2

with open(".env") as f:
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            os.environ[k] = v.strip("'\"")

db_url = os.environ.get("DATABASE_URL", "")

conn2 = psycopg2.connect(db_url)
cursor = conn2.cursor()
cursor.execute('SELECT id, user_id, status FROM "Interviews_table" ORDER BY id DESC LIMIT 1')
row = cursor.fetchone()
if not row:
    print("No interview found")
    sys.exit(0)

interview_id, user_id, status = row
print(f"Latest interview: {interview_id}, User: {user_id}, Status: {status}")

config = {"configurable": {"user_id": str(user_id), "thread_id": str(interview_id)}}
state_snapshot = copilot_workflow.get_state(config)
print("Tasks:", state_snapshot.tasks)
if state_snapshot.tasks:
    if state_snapshot.tasks[0].error:
        print("Error in task:", state_snapshot.tasks[0].error)
    print("Interrupts:", state_snapshot.tasks[0].interrupts)
