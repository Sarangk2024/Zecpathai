# tests/test_ui.py

import os
import sqlite3
from fastapi.testclient import TestClient
from main import app, init_db, db_execute, db_query

client = TestClient(app)

# Run database setup before tests
init_db()

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "ZECPATH" in response.text
    assert "Sign In" in response.text

def test_auth_and_profile_flow():
    # 1. Register Candidate
    reg_payload = {
        "name": "Arjun Nair",
        "email": "arjun@example.com",
        "password": "securepassword",
        "user_type": "candidate"
    }
    response = client.post("/api/auth/register", json=reg_payload)
    # Could be 200 or 400 if already exists, handle gracefully
    assert response.status_code in [200, 400]

    # 2. Login Candidate
    login_payload = {
        "email": "arjun@example.com",
        "password": "securepassword",
        "user_type": "candidate"
    }
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 200
    user_data = response.json()
    cand_id = user_data["user_id"]
    assert user_data["email"] == "arjun@example.com"

    # 3. Save Candidate Profile
    prof_payload = {
        "candidate_id": cand_id,
        "name": "Arjun Nair",
        "contact_info": "+1-555-0199",
        "gender": "Male",
        "location": "Boston, USA",
        "notice_period": "30 days",
        "expected_salary": 95000,
        "skills": "react, node.js, express, mongodb, javascript",
        "experience": 3,
        "resume_text": "Arjun Nair is a Software Engineer expert in React, Node.js, Express, and MongoDB."
    }
    response = client.post("/api/candidates/profile/save", json=prof_payload)
    assert response.status_code == 200

def test_job_and_application_funnel():
    # 1. Get Jobs List
    response = client.get("/api/jobs/list")
    assert response.status_code == 200
    jobs = response.json()
    assert len(jobs) > 0
    job_id = jobs[0]["id"]

    # 2. Register candidate for apply
    reg_payload = {
        "name": "Test Candidate",
        "email": "testcand@example.com",
        "password": "password",
        "user_type": "candidate"
    }
    client.post("/api/auth/register", json=reg_payload)
    
    login_res = client.post("/api/auth/login", json={"email": "testcand@example.com", "password": "password", "user_type": "candidate"})
    cand_id = login_res.json()["user_id"]

    # 3. Apply to Job
    apply_payload = {
        "candidate_id": cand_id,
        "job_id": job_id,
        "name": "Test Candidate",
        "contact_info": "+1-555-0100",
        "gender": "Male",
        "location": "Boston, USA",
        "notice_period": "30 days",
        "expected_salary": 90000,
        "experience": 2,
        "resume_text": "Test Candidate is expert in React, Node.js, Express, and MongoDB."
    }
    response = client.post("/api/apply", json=apply_payload)
    assert response.status_code == 200
    app_data = response.json()
    assert app_data["ats_score"] >= 60.0
    assert app_data["status"] == "shortlisted"
    app_id = app_data["id"]

    # 4. Submit Screening Responses
    screen_payload = {
        "application_id": app_id,
        "screening_score": 85.0,
        "transcript": "AI: Self intro? User: I am a dev. AI: Notice? User: 30 days."
    }
    response = client.post("/api/applications/screening/submit", json=screen_payload)
    assert response.status_code == 200

    # 5. Submit Assessment Scores
    assess_payload = {
        "application_id": app_id,
        "score": 90.0
    }
    response = client.post("/api/applications/assessment/submit", json=assess_payload)
    assert response.status_code == 200

    # 6. Recruiter Pipeline check
    response = client.get("/api/recruiter/pipeline")
    assert response.status_code == 200
    pipeline = response.json()
    assert len(pipeline) > 0

    # 7. Recruiter Override Decision
    override_payload = {
        "application_id": app_id,
        "decision": "Selected"
    }
    response = client.post("/api/recruiter/override", json=override_payload)
    assert response.status_code == 200
