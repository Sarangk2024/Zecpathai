# ai_core/cross_round_engine.py

# -------------------------------
# Default Weights (All Rounds)
# -------------------------------
DEFAULT_WEIGHTS = {
    "ats": 0.20,
    "screening": 0.15,
    "hr": 0.20,
    "technical": 0.25,
    "machine_test": 0.20
}

# -------------------------------
# Role-Based Weight Adjustments
# -------------------------------
ROLE_WEIGHTS = {
    "fresher": {
        "ats": 0.20,
        "screening": 0.20,
        "hr": 0.25,
        "technical": 0.20,
        "machine_test": 0.15
    },
    "experienced": {
        "ats": 0.25,
        "screening": 0.10,
        "hr": 0.20,
        "technical": 0.25,
        "machine_test": 0.20
    },
    "technical": {
        "ats": 0.15,
        "screening": 0.10,
        "hr": 0.15,
        "technical": 0.35,
        "machine_test": 0.25
    },
    "non_technical": {
        "ats": 0.25,
        "screening": 0.20,
        "hr": 0.35,
        "technical": 0.10,
        "machine_test": 0.10
    }
}

def get_weights(role_type=None):
    return ROLE_WEIGHTS.get(role_type, DEFAULT_WEIGHTS)

# -------------------------------
# Unified Score Calculation
# -------------------------------
def calculate_final_score(scores, weights):
    """
    scores = {
        "ats": 70,
        "screening": 75,
        "hr": 80,
        "technical": 85,
        "machine_test": 78
    }
    """
    final = 0
    for key in weights:
        final += scores.get(key, 0) * weights[key]
    return round(final, 2)

# -------------------------------
# Normalization Logic
# -------------------------------
def normalize_scores(scores):
    normalized = {}
    for k, v in scores.items():
        normalized[k] = max(min(v, 100), 0)
    return normalized

# -------------------------------
# Cross-Round Pipeline
# -------------------------------
from ai_core.hiring_fit_calculator import calculate_hiring_fit

def aggregation_pipeline(candidate_id, scores, role_type="technical"):
    normalized_scores = normalize_scores(scores)
    weights = get_weights(role_type)
    final_score = calculate_final_score(normalized_scores, weights)
    fit = calculate_hiring_fit(final_score)
    decision = (
        "Hire" if final_score >= 75 else
        "Consider" if final_score >= 55 else
        "Reject"
    )
    return {
        "candidate_id": candidate_id,
        "scores": normalized_scores,
        "weights": weights,
        "final_score": final_score,
        "decision": decision,
        "hiring_fit": fit
    }
