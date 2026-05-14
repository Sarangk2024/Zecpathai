# tests/test_behavior_analysis.py

from interview_ai.behavior_analyzer import analyze_behavior
from interview_ai.confidence_analyzer import calculate_confidence
from interview_ai.sentiment_engine import sentiment_score
from interview_ai.contradiction_detector import detect_contradiction
from interview_ai.stress_detector import stress_score

def test_behavior():
    result = analyze_behavior("I am confident", 5)
    assert result["behavioral_score"] > 0

def test_confident_metrics():
    text = "I am very confident that we had great success on that project."
    res = analyze_behavior(text, 5) # 12 words / 5s = 2.4 wps (ideal)
    assert res["confidence"]["confidence_score"] >= 80.0
    assert res["sentiment"]["sentiment"] == "Positive"
    assert res["stress_score"] == 1.0
    assert res["contradiction"] is False

def test_stressed_and_contradiction():
    text = "I have experience but actually i don't know, sorry."
    res = analyze_behavior(text, 5)
    assert res["contradiction"] is True
    assert res["stress_score"] < 1.0
