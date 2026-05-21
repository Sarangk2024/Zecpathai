# ai_core/unified_scoring_engine.py

# -------------------------------
# Default Cross-Round Weights
# -------------------------------
DEFAULT_WEIGHTS = {
    "ats": 0.30,
    "screening": 0.30,
    "hr": 0.40
}

# -------------------------------
# Role-Based Weight Adjustment
# -------------------------------
ROLE_BASED_WEIGHTS = {
    "fresher": {
        "ats": 0.25,
        "screening": 0.35,
        "hr": 0.40
    },
    "experienced": {
        "ats": 0.35,
        "screening": 0.25,
        "hr": 0.40
    },
    "technical": {
        "ats": 0.40,
        "screening": 0.30,
        "hr": 0.30
    },
    "non_technical": {
        "ats": 0.20,
        "screening": 0.30,
        "hr": 0.50
    }
}

def get_weights(candidate_type=None):
    return ROLE_BASED_WEIGHTS.get(candidate_type, DEFAULT_WEIGHTS)

# -------------------------------
# Unified Score Calculation
# -------------------------------
def calculate_unified_score(ats_score, screening_score, hr_score, weights):
    final_score = (
        ats_score * weights["ats"] +
        screening_score * weights["screening"] +
        hr_score * weights["hr"]
    )
    return round(final_score, 2)

# -------------------------------
# Unified Scoring Pipeline
# -------------------------------
from ai_core.hiring_fit import calculate_hiring_fit

def unified_scoring_pipeline(candidate_id, ats, screening, hr, candidate_type="fresher"):
    weights = get_weights(candidate_type)
    final_score = calculate_unified_score(
        ats_score=ats,
        screening_score=screening,
        hr_score=hr,
        weights=weights
    )
    fit = calculate_hiring_fit(final_score)
    decision = (
        "Hire" if final_score >= 75 else
        "Consider" if final_score >= 55 else
        "Reject"
    )
    return {
        "candidate_id": candidate_id,
        "final_score": final_score,
        "decision": decision,
        "weights_used": weights,
        "fit": fit
    }
