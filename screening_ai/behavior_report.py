# screening_ai/behavior_report.py

from screening_ai.confidence_engine import calculate_confidence
from screening_ai.sentiment_engine import detect_sentiment
from screening_ai.behavior_rules import detect_uncertainty, detect_contradiction

def generate_behavior_report(answer_text, duration_seconds):
    confidence = calculate_confidence(answer_text, duration_seconds)
    sentiment = detect_sentiment(answer_text)
    uncertainty = detect_uncertainty(answer_text)
    contradiction = detect_contradiction(answer_text)
    return {
        "confidence": confidence,
        "sentiment": sentiment,
        "behavior_flags": {
            "uncertainty": uncertainty,
            "contradiction": contradiction
        },
        "communication_strength": calculate_strength(confidence, sentiment)
    }

def calculate_strength(confidence, sentiment):
    score = (
        confidence["confidence_score"] * 0.6 +
        sentiment["sentiment_score"] * 0.4
    )
    if score >= 0.75:
        return "Strong"
    elif score >= 0.5:
        return "Moderate"
    return "Weak"
