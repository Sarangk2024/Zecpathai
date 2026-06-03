# ai_core/final_production_system.py

# -------------------------------
# Unified Score Normalization
# -------------------------------
def normalize_score(value):
    try:
        value = float(value)
    except:
        return 0.0
    return max(0.0, min(value, 100.0))

# -------------------------------
# Consistency Smoothing
# -------------------------------
def smooth_scores(scores):
    values = [normalize_score(v) for v in scores.values()]
    if not values:
        return scores
    avg = sum(values) / len(values)
    smoothed = {}
    for k, v in scores.items():
        v = normalize_score(v)
        # Apply 70% weight to specific score + 30% weight to candidate average to smooth outliers
        smoothed[k] = round((v * 0.7) + (avg * 0.3), 2)
    return smoothed

# -------------------------------
# Final Decision (Stable + Clear)
# -------------------------------
def final_decision(score):
    if score >= 80:
        return "Selected"
    elif score >= 60:
        return "Hold / Review"
    return "Rejected"

# -------------------------------
# Production Pipeline
# -------------------------------
def production_pipeline(candidate_id, scores):
    smoothed = smooth_scores(scores)
    final_score = round(sum(smoothed.values()) / len(smoothed), 2) if smoothed else 0.0
    decision = final_decision(final_score)
    return {
        "candidate_id": candidate_id,
        "scores": smoothed,
        "final_score": final_score,
        "decision": decision,
        "status": "production_ready"
    }
