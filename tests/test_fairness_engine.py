# tests/test_fairness_engine.py - Unit tests for fairness, masking, and normalization engines.

from ats_engine.fairness_engine import (
    normalize_scores, mask_sensitive_data, 
    reduce_keyword_bias, generate_fair_score
)
from parsers.normalization import normalize_resume_text

def test_normalization():
    candidates = [
        {"final_score": 50},
        {"final_score": 100}
    ]
    result = normalize_scores(candidates)
    assert result[0]["normalized_score"] == 0.0
    assert result[1]["normalized_score"] == 100.0

def test_mask_sensitive_data():
    candidate = {
        "candidate_id": "C123",
        "name": "Sarang K",
        "gender": "Male",
        "location": "Kerala",
        "skill_score": 90
    }
    masked = mask_sensitive_data(candidate)
    assert masked["name"] == "MASKED"
    assert masked["gender"] == "MASKED"
    assert masked["location"] == "MASKED"
    assert masked["skill_score"] == 90

def test_reduce_keyword_bias():
    skill_score = 90
    semantic_score = 80
    fair_score = reduce_keyword_bias(skill_score, semantic_score)
    # 0.6*80 + 0.4*90 = 48 + 36 = 84.0
    assert fair_score == 84.0

def test_generate_fair_score():
    candidate = {
        "candidate_id": "C123",
        "skill_score": 90,
        "semantic_score": 80
    }
    result = generate_fair_score(candidate)
    assert result["fair_score"] == 84.0

def test_normalize_resume_text():
    text = "PROFESSIONAL EXPERIENCE: Worked at Wipro. SKILL SET: Python, React."
    normalized = normalize_resume_text(text)
    assert "experience" in normalized
    assert "skills" in normalized
    assert "professional experience" not in normalized
