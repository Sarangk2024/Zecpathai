# interview_ai/hr_scoring_engine.py

# -------------------------------
# Default Weight Configuration
# -------------------------------
DEFAULT_WEIGHTS = {
    "relevance": 0.30,
    "communication": 0.25,
    "confidence": 0.25,
    "consistency": 0.20
}

# -------------------------------
# Consistency Score
# -------------------------------
def score_consistency(answer):
    if answer.get("contradiction"):
        return 0.3
    if answer.get("is_vague"):
        return 0.6
    return 1.0

# -------------------------------
# Per-Answer Scoring
# -------------------------------
def score_hr_answer(answer, weights=DEFAULT_WEIGHTS):
    relevance = answer.get("relevance_score", 0.7)
    
    # Check if raw communication / confidence scores are out of 100 or fractional
    comm_raw = answer.get("communication_score", 70.0)
    comm_score = comm_raw / 100.0 if comm_raw > 1.0 else comm_raw
    
    conf_raw = answer.get("confidence_score", 70.0)
    conf_score = conf_raw / 100.0 if conf_raw > 1.0 else conf_raw
    
    consistency = score_consistency(answer)
    
    final = (
        relevance * weights["relevance"] +
        comm_score * weights["communication"] +
        conf_score * weights["confidence"] +
        consistency * weights["consistency"]
    )
    
    return {
        "question_id": answer["question_id"],
        "scores": {
            "relevance": round(relevance, 2),
            "communication": round(comm_score, 2),
            "confidence": round(conf_score, 2),
            "consistency": round(consistency, 2)
        },
        "final_score": round(final * 100, 2)
    }

# -------------------------------
# Aggregate HR Interview Score
# -------------------------------
def aggregate_hr_scores(scored_answers):
    if not scored_answers:
        return 0.0
    total = sum(a["final_score"] for a in scored_answers)
    avg = total / len(scored_answers)
    return round(avg, 2)

# -------------------------------
# HR Scoring Pipeline
# -------------------------------
from interview_ai.hr_weights import get_weights

def hr_scoring_pipeline(answers, candidate_type="fresher"):
    weights = get_weights(candidate_type)
    scored = []
    
    for ans in answers:
        result = score_hr_answer(ans, weights)
        scored.append(result)
        
    final_score = aggregate_hr_scores(scored)
    
    decision = (
        "Strong Hire" if final_score >= 75 else
        "Consider" if final_score >= 55 else
        "Reject"
    )
    
    return {
        "hr_score": final_score,
        "decision": decision,
        "details": scored
    }
