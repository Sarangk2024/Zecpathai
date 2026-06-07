# tests/test_ui.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "ZECPATH" in response.text
    assert "Apply Job" in response.text

def test_api_apply():
    payload = {
        "role_key": "mern",
        "resume_text": "Arjun Nair has experience with React and Node.js. Skilled in Javascript and Mongodb."
    }
    response = client.post("/api/apply", data=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Arjun Nair"
    assert data["ats_score"] >= 60.0
    assert "React" in data["skills"]

def test_api_assessment_evaluate_coding():
    payload = {
        "role_key": "mern",
        "code_content": "function reverse(str) { return str.split('').reverse().join(''); }",
        "aptitude_answer": ""
    }
    response = client.post("/api/assessment/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 100.0
    assert "works" in data["message"].lower()

def test_api_assessment_evaluate_aptitude():
    payload = {
        "role_key": "sales",
        "code_content": "",
        "aptitude_answer": "B"
    }
    response = client.post("/api/assessment/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 100.0
    
    payload_wrong = {
        "role_key": "sales",
        "code_content": "",
        "aptitude_answer": "A"
    }
    response_wrong = client.post("/api/assessment/evaluate", json=payload_wrong)
    assert response_wrong.status_code == 200
    data_wrong = response_wrong.json()
    assert data_wrong["score"] == 0.0

def test_api_negotiate_agreed():
    payload = {
        "role_key": "mern",
        "expected_salary": 95000.0,
        "counter_offer_count": 1
    }
    response = client.post("/api/negotiate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "agreed"
    assert data["salary"] == 95000.0

def test_api_negotiate_counter():
    payload = {
        "role_key": "mern",
        "expected_salary": 140000.0,
        "counter_offer_count": 1
    }
    response = client.post("/api/negotiate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "counter"
    assert data["salary"] < 140000.0
