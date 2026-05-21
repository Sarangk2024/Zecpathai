# interview_ai/stable_hr_ai.py

# -------------------------------
# Stabilized Scoring Thresholds
# -------------------------------
DECISION_THRESHOLDS = {
    "hire": 75,
    "consider": 55
}

# -------------------------------
# Smoothed Score Adjustment
# -------------------------------
def smooth_score(scores):
    if not scores:
        return 0
    avg = sum(scores) / len(scores)
    # Remove extreme outliers (scores deviatng more than 20 from average)
    filtered = [s for s in scores if abs(s - avg) <= 20]
    return round(sum(filtered) / len(filtered), 2) if filtered else avg

# -------------------------------
# Stable Decision Logic
# -------------------------------
def stable_decision(score):
    if score >= DECISION_THRESHOLDS["hire"]:
        return "Hire"
    elif score >= DECISION_THRESHOLDS["consider"]:
        return "Consider"
    return "Reject"

# -------------------------------
# Final Stable HR Evaluation
# -------------------------------
def stable_hr_evaluation(scores):
    smoothed = smooth_score(scores)
    decision = stable_decision(smoothed)
    return {
        "stable_score": smoothed,
        "decision": decision
    }
