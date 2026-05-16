# tests/test_system_finalization.py

import json
from api.routes import app
from demo.run_demo import run_demo

def test_routes():
    client = app.test_client()
    payload = {
        "candidate_id": "C101",
        "job_id": "J501",
        "answers": [
            {
                "question_id": "Q1",
                "original_text": "I am a Python developer",
                "skills": ["Python"],
                "availability": "Immediate",
                "salary": "6 LPA",
                "is_vague": False,
                "off_topic": False
            }
        ],
        "scores": [
            {
                "question_id": "Q1",
                "final_score": 85
            }
        ],
        "behavior": [
            {
                "communication_strength": "Strong"
            }
        ]
    }
    response = client.post("/screening/start", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["candidate_id"] == "C101"
    assert data["final_score"] == 85.0
    assert data["decision"] == "Proceed"

def test_demo():
    report = run_demo()
    assert report["candidate_id"] == "C1001"
    assert report["decision"] == "Proceed"
