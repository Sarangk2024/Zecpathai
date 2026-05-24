# tests/test_behavioral_ai.py

from behavior_ai.signal_mapping import calculate_behavior_score, detect_behavior_risk

def test_behavior_score():
    # Specifications-requested test structure
    result = calculate_behavior_score({
        "eye_focus": 0.7,
        "head_stability": 0.7,
        "engagement": 0.7,
        "distraction": 0.3
    })
    assert result > 0

def test_behavior_scoring_math():
    # focus*0.3 + head*0.2 + engagement*0.3 + (1-distraction)*0.2
    # 0.8*0.3 + 0.7*0.2 + 0.9*0.3 + (1-0.2)*0.2
    # = 0.24 + 0.14 + 0.27 + 0.8*0.2
    # = 0.24 + 0.14 + 0.27 + 0.16 = 0.81 -> * 100 = 81.0
    signals = {
        "eye_focus": 0.8,
        "head_stability": 0.7,
        "engagement": 0.9,
        "distraction": 0.2
    }
    assert calculate_behavior_score(signals) == 81.0

def test_detect_behavior_risk():
    assert detect_behavior_risk(85) == "Low Risk"
    assert detect_behavior_risk(65) == "Moderate Risk"
    assert detect_behavior_risk(45) == "High Risk"
