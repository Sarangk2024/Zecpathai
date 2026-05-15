# tests/test_system_optimization.py

from screening_ai.improved_intent import improved_intent_classification, get_decision
from screening_ai.optimized_flow_updates import adaptive_retry_logic

def test_intent():
    text = "I worked as a developer for 2 years"
    result = improved_intent_classification(text)
    assert result == "experience"

def test_decisions():
    assert get_decision(70) == "Pass"
    assert get_decision(55) == "Review"
    assert get_decision(30) == "Reject"

def test_adaptive_retry():
    assert adaptive_retry_logic("silence", 0) == "retry"
    assert adaptive_retry_logic("silence", 1) == "simplify_question"
    assert adaptive_retry_logic("silence", 2) == "skip_question"
    assert adaptive_retry_logic("confusion", 0) == "clarify"
    assert adaptive_retry_logic("repeat", 0) == "ask_example"
    assert adaptive_retry_logic("valid", 0) == "next"
