# ats_engine/ats_scorer.py - ATS scoring engine with configurable weight profiles for Zecpath AI.

# -------------------------------
# Default Weight Configuration
# -------------------------------
DEFAULT_WEIGHTS = {
    "skills": 0.35,
    "experience": 0.25,
    "education": 0.15,
    "semantic": 0.25
}

# -------------------------------
# Role-Based Weights (Tech & Manufacturing)
# -------------------------------
ROLE_WEIGHTS = {
    "backend developer": {
        "skills": 0.40,
        "experience": 0.30,
        "education": 0.10,
        "semantic": 0.20
    },
    "data scientist": {
        "skills": 0.35,
        "experience": 0.25,
        "education": 0.20,
        "semantic": 0.20
    },
    "marketing executive": {
        "skills": 0.30,
        "experience": 0.30,
        "education": 0.15,
        "semantic": 0.25
    },
    
    # Tool & Die / Manufacturing trade profiles
    "tool maker": {
        "skills": 0.40,
        "experience": 0.30,
        "education": 0.10,
        "semantic": 0.20
    },
    "trainee tool die maker": {
        "skills": 0.30,
        "experience": 0.20,
        "education": 0.30,
        "semantic": 0.20
    },
    "die design engineer": {
        "skills": 0.35,
        "experience": 0.35,
        "education": 0.15,
        "semantic": 0.15
    },
    "mold design engineer": {
        "skills": 0.35,
        "experience": 0.35,
        "education": 0.15,
        "semantic": 0.15
    },
    "cnc machinist": {
        "skills": 0.45,
        "experience": 0.30,
        "education": 0.10,
        "semantic": 0.15
    }
}

# -------------------------------
# Normalize Score (0-100 -> 0-1)
# -------------------------------
def normalize(score):
    return score / 100.0 if score else 0.0

# -------------------------------
# Safe score utility
# -------------------------------
def safe_score(value):
    return value if value is not None else 0.0

# -------------------------------
# Dynamic Weight Lookup
# -------------------------------
def get_weights(job_role):
    if not job_role:
        return DEFAULT_WEIGHTS
    role_lower = job_role.lower().strip()
    return ROLE_WEIGHTS.get(role_lower, DEFAULT_WEIGHTS)

# -------------------------------
# ATS Score Calculation
# -------------------------------
def calculate_ats_score(candidate, job, weights=DEFAULT_WEIGHTS):
    skill_score = normalize(safe_score(candidate.get("skill_score")))
    exp_score = normalize(safe_score(candidate.get("experience_score")))
    edu_score = normalize(safe_score(candidate.get("education_score")))
    semantic_score = normalize(safe_score(candidate.get("semantic_score")))
    
    final_score = (
        weights["skills"] * skill_score +
        weights["experience"] * exp_score +
        weights["education"] * edu_score +
        weights["semantic"] * semantic_score
    )
    return round(final_score * 100, 2)

# -------------------------------
# Candidate Score Generator
# -------------------------------
def generate_candidate_score(candidate, job):
    weights = get_weights(job.get("job_title", ""))
    final_score = calculate_ats_score(candidate, job, weights)
    return {
        "candidate_id": candidate.get("candidate_id"),
        "final_score": final_score,
        "weights_used": weights,
        "breakdown": {
            "skill_score": safe_score(candidate.get("skill_score")),
            "experience_score": safe_score(candidate.get("experience_score")),
            "education_score": safe_score(candidate.get("education_score")),
            "semantic_score": safe_score(candidate.get("semantic_score"))
        }
    }

# -------------------------------
# Safe ATS scoring interface
# -------------------------------
def calculate_safe_ats(candidate, job):
    candidate_copy = candidate.copy()
    candidate_copy["skill_score"] = safe_score(candidate.get("skill_score"))
    candidate_copy["experience_score"] = safe_score(candidate.get("experience_score"))
    candidate_copy["education_score"] = safe_score(candidate.get("education_score"))
    candidate_copy["semantic_score"] = safe_score(candidate.get("semantic_score"))
    return generate_candidate_score(candidate_copy, job)
