# tests/test_advanced_proposal.py

from future.ai_coach import generate_feedback

def test_ai_coach():
    # Specifications-requested test structure
    feedback = generate_feedback({
        "communication": 60,
        "technical": 80,
        "confidence": 50
    })
    assert len(feedback) > 0
    assert "Improve communication clarity" in feedback
    assert "Work on confidence and delivery" in feedback
    assert "Strengthen technical fundamentals" not in feedback

def test_ai_coach_perfect():
    feedback = generate_feedback({
        "communication": 90,
        "technical": 95,
        "confidence": 90
    })
    assert len(feedback) == 0
