# tests/test_integrity_detection.py

from integrity_ai.risk_engine import calculate_integrity_score, risk_flagging, generate_warning, combined_risk
from integrity_ai.detection_logic import detect_malpractice

def test_integrity():
    # Specifications-requested test structure
    score = calculate_integrity_score({
        "tab_switch": 2,
        "focus_loss": 1,
        "voice_detect": 0,
        "gaze_off": 2
    })
    assert score > 0

def test_integrity_scoring_math():
    # 100 - (2*5) - (3*3) - (1*10) - (4*4)
    # = 100 - 10 - 9 - 10 - 16 = 55
    events = {
        "tab_switch": 2,
        "focus_loss": 3,
        "voice_detect": 1,
        "gaze_off": 4
    }
    assert calculate_integrity_score(events) == 55

def test_risk_flagging():
    assert risk_flagging(80) == "Low Risk"
    assert risk_flagging(65) == "Moderate Risk"
    assert risk_flagging(40) == "High Risk"

def test_generate_warning():
    events = {"tab_switch": 3, "voice_detect": 2, "focus_loss": 4}
    warnings = generate_warning(events)
    assert "Please stay on the interview screen" in warnings
    assert "External voice detected. Please ensure you are alone" in warnings
    assert "You seem distracted. Please focus on the interview" in warnings
    
    # Under limit warnings should be empty
    assert generate_warning({"tab_switch": 1}) == []

def test_combined_risk():
    # 80 * 0.4 + 90 * 0.6 = 32.0 + 54.0 = 86.0
    assert combined_risk(80, 90) == 86.0

def test_detect_malpractice():
    # limit: "tab_switch": 3, "focus_loss": 5, "voice_detect": 2, "gaze_off": 5
    events_malpractice = {
        "tab_switch": 4,
        "focus_loss": 6,
        "voice_detect": 3,
        "gaze_off": 6
    }
    flags = detect_malpractice(events_malpractice)
    assert "High Tab Switching" in flags
    assert "Screen Focus Loss" in flags
    assert "Multiple Voices Detected" in flags
    assert "Frequent Gaze Deviation" in flags
    
    assert detect_malpractice({"tab_switch": 1}) == []
