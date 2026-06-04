# ai_core/release_ready_system.py

# -------------------------------
# Safe Value Handler
# -------------------------------
def safe_value(v, default=0.0):
    try:
        v = float(v)
    except:
        return default
    return max(0.0, min(v, 100.0))

# -------------------------------
# Unified Score Validator
# -------------------------------
def validate_scores(scores):
    return {k: safe_value(v) for k, v in scores.items()}

# -------------------------------
# Stable Aggregation
# -------------------------------
def final_aggregate(scores):
    scores = validate_scores(scores)
    if not scores:
        return 0.0
    return round(sum(scores.values()) / len(scores), 2)

# -------------------------------
# Final Decision Logic (Consistent)
# -------------------------------
def final_decision(score):
    if score >= 80:
        return "Selected"
    elif score >= 60:
        return "Hold / Review"
    return "Rejected"

# -------------------------------
# Release Pipeline
# -------------------------------
def release_pipeline(candidate_id, scores):
    scores = validate_scores(scores)
    final_score = final_aggregate(scores)
    decision = final_decision(final_score)
    return {
        "candidate_id": candidate_id,
        "scores": scores,
        "final_score": final_score,
        "decision": decision,
        "status": "release_ready"
    }
