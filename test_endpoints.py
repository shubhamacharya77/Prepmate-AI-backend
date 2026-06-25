import requests
import json
from service.jwt_token import create_access_token

# 1. Generate a valid token using backend's own function
payload = {"id": 1, "name": "Test User", "email": "test@example.com"}
token = create_access_token(payload)
headers = {"Authorization": f"Bearer {token}"}

base_url = "http://127.0.0.1:8000/api"

print("--- Testing /api/interview_history ---")
res = requests.get(f"{base_url}/interview_history", headers=headers)
print(res.status_code, res.json())

print("\n--- Testing /api/create_interview ---")
res = requests.post(f"{base_url}/create_interview", headers=headers, json={
    "topic": "Python Fundamentals",
    "difficulty_level": "Easy",
    "interview_type": "Technical",
    "status": "Start"
})
print(res.status_code, res.json())

print("\n--- Testing /api/get_interview_questions ---")
res = requests.post(f"{base_url}/get_interview_questions", headers=headers)
print(res.status_code, res.json())

print("\n--- Testing /api/post_question_answer ---")
res = requests.post(f"{base_url}/post_question_answer", headers=headers, json={"answer": "Python is a high level language."})
print(res.status_code, res.json())

print("\n--- Testing /api/interview_history (again) ---")
res = requests.get(f"{base_url}/interview_history", headers=headers)
history = res.json().get("history", [])
print(res.status_code, history)

if history:
    latest_id = history[-1]["id"]
    print(f"\n--- Testing /api/interview_details/{latest_id} ---")
    res = requests.get(f"{base_url}/interview_details/{latest_id}", headers=headers)
    print(res.status_code, str(res.json())[:200] + "...")

    print(f"\n--- Testing /api/generate_interview_report/{latest_id} ---")
    res = requests.post(f"{base_url}/generate_interview_report/{latest_id}", headers=headers)
    print(res.status_code, res.json())
