# integrity_ai/risk_engine.py

def calculate_integrity_score(events):
    score = 100
    score -= events.get("tab_switch", 0) * 5
    score -= events.get("focus_loss", 0) * 3
    score -= events.get("voice_detect", 0) * 10
    score -= events.get("gaze_off", 0) * 4
    return max(score, 0)

def risk_flagging(score):
    if score < 50:
        return "High Risk"
    elif score < 75:
        return "Moderate Risk"
    return "Low Risk"

def generate_warning(events):
    warnings = []
    if events.get("tab_switch", 0) > 2:
        warnings.append("Please stay on the interview screen")
    if events.get("voice_detect", 0) > 1:
        warnings.append("External voice detected. Please ensure you are alone")
    if events.get("focus_loss", 0) > 3:
        warnings.append("You seem distracted. Please focus on the interview")
    return warnings

def combined_risk(behavior_score, integrity_score):
    final = (behavior_score * 0.4) + (integrity_score * 0.6)
    return round(final, 2)
