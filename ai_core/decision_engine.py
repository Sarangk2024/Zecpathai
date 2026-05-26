# ai_core/decision_engine.py

# -------------------------------
# Decision Thresholds
# -------------------------------
THRESHOLDS = {
    "selected": 80,
    "hold": 60
}

# -------------------------------
# Risk Weight Adjustment
# -------------------------------
def adjust_for_risk(score, behavior_risk, integrity_risk):
    penalty = 0
    if behavior_risk == "High Risk":
        penalty += 10
    elif behavior_risk == "Moderate Risk":
        penalty += 5
        
    if integrity_risk == "High Risk":
        penalty += 15
    elif integrity_risk == "Moderate Risk":
        penalty += 7
        
    return max(score - penalty, 0)

# -------------------------------
# Decision Logic
# -------------------------------
def generate_decision(final_score, behavior_risk="Low Risk", integrity_risk="Low Risk"):
    adjusted_score = adjust_for_risk(final_score, behavior_risk, integrity_risk)
    if adjusted_score >= THRESHOLDS["selected"]:
        decision = "Selected"
    elif adjusted_score >= THRESHOLDS["hold"]:
        decision = "Hold / Review"
    else:
        decision = "Rejected"
    return decision, adjusted_score

# -------------------------------
# Confidence Score Calculation
# -------------------------------
def calculate_decision_confidence(scores):
    """
    scores = list of stage scores
    """
    if not scores:
        return 0
    variance = max(scores) - min(scores)
    confidence = max(100 - variance, 50)
    return round(confidence, 2)

# -------------------------------
# Recommendation Logic (Pipeline)
# -------------------------------
def recommendation_pipeline(candidate_id, scores, behavior_risk, integrity_risk):
    final_score = scores.get("final_score", 0)
    decision, adjusted_score = generate_decision(
        final_score,
        behavior_risk,
        integrity_risk
    )
    # Exclude final_score if present in keys
    stage_scores = [v for k, v in scores.items() if k != "final_score"]
    confidence = calculate_decision_confidence(stage_scores)
    explanation = generate_explanation(scores, decision)
    return {
        "candidate_id": candidate_id,
        "final_score": final_score,
        "adjusted_score": adjusted_score,
        "decision": decision,
        "confidence_score": confidence,
        "risks": {
            "behavior": behavior_risk,
            "integrity": integrity_risk
        },
        "explanation": explanation
    }

# -------------------------------
# Explainable Output Generator
# -------------------------------
def generate_explanation(scores, decision):
    strengths = []
    weaknesses = []
    
    if scores.get("technical", 0) > 80:
        strengths.append("Strong technical skills")
    if scores.get("communication", 0) > 75 or scores.get("hr", 0) > 75:
        strengths.append("Good communication")
        
    if scores.get("behavior", 100) < 60:
        weaknesses.append("Behavioral concerns")
    if scores.get("integrity", 100) < 60:
        weaknesses.append("Integrity risks")
        
    reason = "Strong overall performance"
    if decision == "Hold / Review":
        reason = "Moderate performance, requires review"
    elif decision == "Rejected":
        reason = "Low score with high risk factors"
        
    return {
        "reason": reason,
        "strengths": strengths,
        "weaknesses": weaknesses
    }
