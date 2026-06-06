# tests/test_ui.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "ZECPATH" in response.text
    assert "Simulate Candidate" in response.text

def test_api_simulate_selected():
    payload = {
        "candidate_id": "C_TEST_01",
        "name": "Test Strong",
        "ats_score": 90.0,
        "screening_score": 90.0,
        "hr_score": 90.0,
        "technical_score": 90.0,
        "machine_test_score": 90.0,
        "behavior_risk": "Low Risk",
        "integrity_risk": "Low Risk"
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["candidate_id"] == "C_TEST_01"
    assert data["final_score"] == 90.0
    assert data["decision"] == "Selected"

def test_api_simulate_rejected_with_risks():
    payload = {
        "candidate_id": "C_TEST_02",
        "name": "Test Weak",
        "ats_score": 50.0,
        "screening_score": 50.0,
        "hr_score": 50.0,
        "technical_score": 50.0,
        "machine_test_score": 50.0,
        "behavior_risk": "High Risk", # -20 deduction
        "integrity_risk": "High Risk" # -30 deduction
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["candidate_id"] == "C_TEST_02"
    # 50.0 - 20 - 30 = 0.0
    assert data["final_score"] == 0.0
    assert data["decision"] == "Rejected"
