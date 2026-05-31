# interview_ai/hr_weights.py

ROLE_WEIGHTS = {
    "fresher": {
        "relevance": 0.25,
        "communication": 0.30,
        "confidence": 0.25,
        "consistency": 0.20
    },
    "experienced": {
        "relevance": 0.35,
        "communication": 0.20,
        "confidence": 0.25,
        "consistency": 0.20
    }
}

def get_weights(candidate_type):
    return ROLE_WEIGHTS.get(candidate_type, ROLE_WEIGHTS["fresher"])

def normalize_interview_score(score, total_questions):
    if total_questions == 0:
        return 0.0
    normalized = score / total_questions
    return round(normalized, 2)
