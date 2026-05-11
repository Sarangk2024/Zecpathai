# tests/test_eligibility_engine.py - Unit tests for candidate eligibility engine.

import pytest
from screening_ai.eligibility_engine import evaluate_candidate, evaluate_candidates_batch

def test_eligibility():
    candidate = {
        "candidate_id": "C123",
        "final_score": 80,
        "skills": ["Python"],
        "total_experience": 3
    }
    rules = {
        "min_ats_score": 70,
        "mandatory_skills": ["Python"],
        "min_experience": 2,
        "max_experience": 5,
        "allowed_locations": [],
        "availability_required": False
    }
    result = evaluate_candidate(candidate, rules)
    assert result["eligibility_status"] == "Eligible"
    assert result["checks"]["ats_score"] == 80
    assert result["checks"]["skill_match"] is True
    assert result["checks"]["experience_match"] is True

def test_eligibility_review():
    candidate = {
        "candidate_id": "C124",
        "final_score": 60,  # Below min 70, but within 15 points buffer
        "skills": ["Python"],
        "total_experience": 3
    }
    rules = {
        "min_ats_score": 70,
        "mandatory_skills": ["Python"],
        "min_experience": 2,
        "max_experience": 5,
        "allowed_locations": [],
        "availability_required": False
    }
    result = evaluate_candidate(candidate, rules)
    assert result["eligibility_status"] == "Review"

def test_eligibility_rejected_score():
    candidate = {
        "candidate_id": "C125",
        "final_score": 50,  # Below 15 point buffer
        "skills": ["Python"],
        "total_experience": 3
    }
    rules = {
        "min_ats_score": 70,
        "mandatory_skills": ["Python"],
        "min_experience": 2,
        "max_experience": 5,
        "allowed_locations": [],
        "availability_required": False
    }
    result = evaluate_candidate(candidate, rules)
    assert result["eligibility_status"] == "Rejected"

def test_eligibility_rejected_skills():
    candidate = {
        "candidate_id": "C126",
        "final_score": 85,
        "skills": ["Java"],  # Missing mandatory Python
        "total_experience": 3
    }
    rules = {
        "min_ats_score": 70,
        "mandatory_skills": ["Python"],
        "min_experience": 2,
        "max_experience": 5,
        "allowed_locations": [],
        "availability_required": False
    }
    result = evaluate_candidate(candidate, rules)
    assert result["eligibility_status"] == "Rejected"

def test_batch_evaluation():
    candidates = [
        {"candidate_id": "C1", "final_score": 80, "skills": ["Python"], "total_experience": 3},
        {"candidate_id": "C2", "final_score": 40, "skills": ["Python"], "total_experience": 3}
    ]
    rules = {
        "min_ats_score": 70,
        "mandatory_skills": ["Python"],
        "min_experience": 2,
        "max_experience": 5,
        "allowed_locations": [],
        "availability_required": False
    }
    results = evaluate_candidates_batch(candidates, rules)
    assert len(results) == 2
    assert results[0]["eligibility_status"] == "Eligible"
    assert results[1]["eligibility_status"] == "Rejected"
