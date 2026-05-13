# tests/test_screening_scoring.py

from screening_ai.scoring_engine import (
    score_clarity,
    score_relevance,
    score_completeness,
    score_consistency,
    score_answer,
    screening_scoring_pipeline,
    normalize_score,
    explain_score
)

def test_scoring():
    answer = {
        "question_id": "Q3",
        "original_text": "I have 2 years experience",
        "intent": "experience",
        "skills": [],
        "experience_years": 2,
        "availability": "Unknown",
        "off_topic": False,
        "is_vague": False
    }
    result = score_answer(answer, "experience")
    assert result["final_score"] > 50

def test_score_clarity():
    assert score_clarity({"original_text": "hello there"}) == 0.4
    assert score_clarity({"original_text": "hello this is a test script"}) == 0.7
    assert score_clarity({"original_text": "hello this is a long text with many words in it"}) == 1.0
    assert score_clarity({"original_text": "hello"}) == 0.0
    assert score_clarity({"original_text": ""}) == 0.0

def test_score_relevance():
    assert score_relevance({"intent": "experience"}, "experience") == 1.0
    assert score_relevance({"intent": "skills"}, "experience") == 0.3

def test_score_completeness():
    assert score_completeness({"skills": ["python"], "experience_years": 3, "availability": "Immediate"}) == 1.0
    assert score_completeness({"skills": [], "experience_years": 0, "availability": "Unknown"}) == 0.0

def test_score_consistency():
    assert score_consistency({"is_vague": True}) == 0.3
    assert score_consistency({"off_topic": True}) == 0.2
    assert score_consistency({"is_vague": False, "off_topic": False}) == 1.0

def test_pipeline():
    answers = [
        {
            "question_id": "Q3",
            "original_text": "I have 3 years experience in Python",
            "intent": "experience",
            "skills": ["python"],
            "experience_years": 3,
            "availability": "Immediate",
            "off_topic": False,
            "is_vague": False
        }
    ]
    intent_map = {"Q3": "experience"}
    result = screening_scoring_pipeline(answers, intent_map)
    assert "screening_score" in result
    assert result["decision"] in ["Pass", "Review", "Reject"]
    assert len(result["details"]) == 1

def test_normalization():
    assert normalize_score(80, 100) == 80.0
    assert normalize_score(5, 10) == 50.0

def test_explain_score():
    answer = {
        "question_id": "Q3",
        "original_text": "I have 3 years experience in Python",
        "intent": "experience",
        "skills": ["python"],
        "experience_years": 3,
        "availability": "Immediate",
        "off_topic": False,
        "is_vague": False
    }
    scored = score_answer(answer, "experience")
    explanation = explain_score(scored)
    assert explanation["question_id"] == "Q3"
    assert "clarity" in explanation["explanation"]
