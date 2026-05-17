# tests/test_followup.py

from interview_ai.followup_engine import detect_answer_quality, generate_followup
from interview_ai.adaptive_engine import adapt_question_level, generate_adaptive_question
from interview_ai.state_tracker import InterviewState, avoid_repetition
from interview_ai.followup_pipeline import followup_pipeline

def test_followup():
    result = detect_answer_quality("I worked")
    assert result == "too_short"

def test_quality_types():
    assert detect_answer_quality("") == "empty"
    assert detect_answer_quality("I worked in teams") == "basic"
    assert detect_answer_quality("I think I worked.") == "uncertain"
    assert detect_answer_quality("I worked in teams at my previous company doing backend development.") == "good"

def test_generate_followup():
    q = "What is your stack?"
    assert "elaborate" in generate_followup(q, "too_short")
    assert "clarify" in generate_followup(q, "uncertain")
    assert "real example" in generate_followup(q, "basic")
    assert generate_followup(q, "good") is None

def test_adaptive_logic():
    assert adapt_question_level("empty", 0.5) == "simplify"
    assert adapt_question_level("basic", 0.5) == "example"
    assert adapt_question_level("good", 0.8) == "advanced"
    assert adapt_question_level("good", 0.5) == "normal"
    
    q = "Tell me about teamwork"
    assert "simplify" in generate_adaptive_question(q, "simplify")
    assert "real-world example" in generate_adaptive_question(q, "example")
    assert "complex scenario" in generate_adaptive_question(q, "advanced")

def test_state_tracker():
    state = InterviewState()
    assert state.is_repeated("Q1") is False
    state.add_interaction("Q1", "Answer")
    assert state.is_repeated("Q1") is True
    
    pool = ["Q1", "Q2", "Q3"]
    assert avoid_repetition(state, pool) == ["Q2", "Q3"]

def test_pipeline():
    res = followup_pipeline("Tell me about teamwork", "I worked in a team", 0.6)
    assert res["quality"] == "basic"
    assert "real example" in res["followup"]
    assert "real-world example" in res["next_question"]
