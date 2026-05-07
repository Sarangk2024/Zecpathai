# tests/test_ats_scorer.py - Unit tests for ATS scoring engine.

from ats_engine.ats_scorer import (
    calculate_ats_score, get_weights, 
    generate_candidate_score, calculate_safe_ats
)

def test_ats_score():
    candidate = {
        "skill_score": 80,
        "experience_score": 70,
        "education_score": 60,
        "semantic_score": 75
    }
    score = calculate_ats_score(candidate, {})
    assert score > 0
    # Weighted score: 0.35*80 + 0.25*70 + 0.15*60 + 0.25*75 = 28 + 17.5 + 9 + 18.75 = 73.25
    assert score == 73.25

def test_get_weights():
    w_dev = get_weights("Backend Developer")
    assert w_dev["skills"] == 0.40
    
    w_mfg = get_weights("CNC Machinist")
    assert w_mfg["skills"] == 0.45
    
    w_default = get_weights("Random Job Title")
    assert w_default["skills"] == 0.35

def test_generate_candidate_score():
    candidate = {
        "candidate_id": "C123",
        "skill_score": 90,
        "experience_score": 85,
        "education_score": 80,
        "semantic_score": 88
    }
    job = {
        "job_title": "Backend Developer"
    }
    result = generate_candidate_score(candidate, job)
    assert result["candidate_id"] == "C123"
    assert result["final_score"] > 0
    assert result["breakdown"]["skill_score"] == 90

def test_calculate_safe_ats():
    candidate = {
        "candidate_id": "C123",
        "skill_score": None,
        "experience_score": 85
    }
    job = {"job_title": "CNC Machinist"}
    result = calculate_safe_ats(candidate, job)
    assert result["breakdown"]["skill_score"] == 0.0
    assert result["breakdown"]["experience_score"] == 85.0
