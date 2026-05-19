# tests/test_hr_scoring.py

from interview_ai.hr_scoring_engine import hr_scoring_pipeline, score_hr_answer
from interview_ai.hr_weights import get_weights, normalize_interview_score

def test_hr_score():
    result = hr_scoring_pipeline([], "fresher")
    assert "hr_score" in result

def test_weights_assignment():
    fresh_w = get_weights("fresher")
    assert fresh_w["communication"] == 0.30
    
    exp_w = get_weights("experienced")
    assert exp_w["relevance"] == 0.35

def test_score_hr_answer():
    ans = {
        "question_id": "Q1",
        "relevance_score": 0.9,
        "communication_score": 85.0,
        "confidence_score": 80.0,
        "contradiction": False,
        "is_vague": False
    }
    res = score_hr_answer(ans, get_weights("experienced"))
    # relevance*0.35 + comm*0.2 + conf*0.25 + consistency*0.2
    # = 0.9*0.35 + 0.85*0.2 + 0.8*0.25 + 1.0*0.2 = 0.315 + 0.17 + 0.2 + 0.2 = 0.885 -> 88.5
    assert res["final_score"] == 88.50

def test_normalization():
    assert normalize_interview_score(160, 2) == 80.00
    assert normalize_interview_score(0, 0) == 0.0
