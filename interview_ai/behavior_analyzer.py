# interview_ai/behavior_analyzer.py

from interview_ai.confidence_analyzer import calculate_confidence
from interview_ai.sentiment_engine import sentiment_score
from interview_ai.contradiction_detector import detect_contradiction
from interview_ai.stress_detector import stress_score

def analyze_behavior(text, duration):
    confidence = calculate_confidence(text, duration)
    sentiment = sentiment_score(text)
    contradiction = detect_contradiction(text)
    stress = stress_score(text)
    
    final_score = (
        confidence["confidence_score"] * 0.5 +
        sentiment["sentiment_score"] * 100 * 0.2 +
        stress * 100 * 0.3
    )
    
    return {
        "confidence": confidence,
        "sentiment": sentiment,
        "stress_score": stress,
        "contradiction": contradiction,
        "behavioral_score": round(final_score, 2)
    }
