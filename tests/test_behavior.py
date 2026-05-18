# tests/test_behavior.py

from screening_ai.behavior_report import generate_behavior_report
from screening_ai.confidence_engine import calculate_confidence, detect_hesitation
from screening_ai.sentiment_engine import detect_sentiment
from screening_ai.behavior_rules import detect_uncertainty, detect_contradiction

def test_behavior():
    text = "I am confident and experienced"
    result = generate_behavior_report(text, 5)
    assert result["communication_strength"] in ["Strong", "Moderate"]

def test_hesitation_and_confidence():
    text = "um uh like i worked for some time"
    hesitation = detect_hesitation(text)
    assert hesitation > 0
    confidence = calculate_confidence(text, 10)
    assert "confidence_score" in confidence
    assert "signals" in confidence

def test_sentiment():
    pos_res = detect_sentiment("This is a great and strong stack.")
    assert pos_res["sentiment"] == "Positive"
    neg_res = detect_sentiment("I struggle and find it difficult.")
    assert neg_res["sentiment"] == "Negative"

def test_rules():
    assert detect_uncertainty("Maybe next week.") is True
    assert detect_contradiction("I can join, but not immediately.") is True
