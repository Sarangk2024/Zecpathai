# tests/test_decision_ai.py

from ai_core.decision_engine import generate_decision, adjust_for_risk, calculate_decision_confidence, recommendation_pipeline

def test_decision():
    # Specifications-requested test structure
    decision, score = generate_decision(85)
    assert decision == "Selected"
    assert score == 85

def test_adjust_for_risk():
    # No risk -> no penalty
    assert adjust_for_risk(80, "Low Risk", "Low Risk") == 80
    
    # Moderate behavior (+5) and High integrity (+15) -> -20 penalty
    assert adjust_for_risk(80, "Moderate Risk", "High Risk") == 60
    
    # High behavior (+10) and Moderate integrity (+7) -> -17 penalty
    assert adjust_for_risk(90, "High Risk", "Moderate Risk") == 73

def test_calculate_decision_confidence():
    # max - min = 90 - 70 = 20. confidence = 100 - 20 = 80
    assert calculate_decision_confidence([70, 80, 90]) == 80
    
    # max - min = 90 - 30 = 60. confidence = 100 - 60 = 40, fallback to 50 minimum
    assert calculate_decision_confidence([30, 90]) == 50
    
    # empty list
    assert calculate_decision_confidence([]) == 0

def test_recommendation_pipeline():
    scores = {
        "ats": 85,
        "screening": 80,
        "technical": 90,
        "hr": 82,
        "machine_test": 85,
        "final_score": 84
    }
    
    # Moderate integrity -> penalty of 7 -> adjusted score is 77 -> decision Hold / Review
    res = recommendation_pipeline("C10001", scores, "Low Risk", "Moderate Risk")
    assert res["candidate_id"] == "C10001"
    assert res["final_score"] == 84
    assert res["adjusted_score"] == 77
    assert res["decision"] == "Hold / Review"
    assert res["confidence_score"] == 90.0 # max 90, min 80 -> variance 10 -> confidence 90
