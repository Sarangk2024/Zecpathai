# screening_ai/scoring_engine.py

# -------------------------------
# Scoring Weights
# -------------------------------
WEIGHTS = {
    "clarity": 0.25,
    "relevance": 0.30,
    "completeness": 0.25,
    "consistency": 0.20
}

# -------------------------------
# Clarity Score
# -------------------------------
def score_clarity(answer):
    text = answer.get("original_text", "")
    length = len(text.split())
    if length > 8:
        return 1.0
    elif length > 4:
        return 0.7
    elif length > 1:
        return 0.4
    return 0.0

# -------------------------------
# Relevance Score
# -------------------------------
def score_relevance(answer, expected_intent):
    return 1.0 if answer.get("intent") == expected_intent else 0.3

# -------------------------------
# Completeness Score
# -------------------------------
def score_completeness(answer):
    score = 0
    if answer.get("skills"):
        score += 0.4
    # Check both experience_years and greater than zero
    exp = answer.get("experience_years")
    if exp is not None and isinstance(exp, (int, float)) and exp > 0:
        score += 0.3
    availability = answer.get("availability")
    if availability and availability != "Unknown":
        score += 0.3
    return min(score, 1.0)

# -------------------------------
# Consistency Score
# -------------------------------
def score_consistency(answer):
    if answer.get("is_vague"):
        return 0.3
    if answer.get("off_topic"):
        return 0.2
    return 1.0

# -------------------------------
# Per Question Score
# -------------------------------
def score_answer(answer, expected_intent):
    clarity = score_clarity(answer)
    relevance = score_relevance(answer, expected_intent)
    completeness = score_completeness(answer)
    consistency = score_consistency(answer)
    final = (
        clarity * WEIGHTS["clarity"] +
        relevance * WEIGHTS["relevance"] +
        completeness * WEIGHTS["completeness"] +
        consistency * WEIGHTS["consistency"]
    )
    return {
        "question_id": answer["question_id"],
        "scores": {
            "clarity": round(clarity, 2),
            "relevance": round(relevance, 2),
            "completeness": round(completeness, 2),
            "consistency": round(consistency, 2)
        },
        "final_score": round(final * 100, 2)
    }

# -------------------------------
# Aggregate Scoring
# -------------------------------
def aggregate_scores(scored_answers):
    if not scored_answers:
        return 0
    total = sum(a["final_score"] for a in scored_answers)
    avg = total / len(scored_answers)
    return round(avg, 2)

# -------------------------------
# Screening Pipeline Function
# -------------------------------
def screening_scoring_pipeline(answers, intent_map):
    scored_answers = []
    for ans in answers:
        expected_intent = intent_map.get(ans["question_id"], "unknown")
        scored = score_answer(ans, expected_intent)
        scored_answers.append(scored)
    final_score = aggregate_scores(scored_answers)
    decision = "Pass" if final_score >= 70 else "Review" if final_score >= 50 else "Reject"
    return {
        "screening_score": final_score,
        "decision": decision,
        "details": scored_answers
    }

# -------------------------------
# Score Normalization
# -------------------------------
def normalize_score(score, max_score=100):
    return round((score / max_score) * 100, 2)

# -------------------------------
# Explainable Scoring Output
# -------------------------------
def explain_score(scored_answer):
    scores = scored_answer["scores"]
    clarity_exp = "Answer is detailed and well-structured" if scores["clarity"] >= 0.7 else "Answer is brief or incomplete"
    relevance_exp = "Matches expected intent" if scores["relevance"] == 1.0 else "Does not match expected intent"
    
    if scores["completeness"] == 1.0:
        completeness_exp = "Fully complete with all required information"
    elif scores["completeness"] >= 0.7:
        completeness_exp = "Includes skills and experience but missing salary"
    else:
        completeness_exp = "Missing critical details"
        
    consistency_exp = "No vague or off-topic indicators" if scores["consistency"] == 1.0 else "Vague or off-topic indicators present"
    
    return {
        "question_id": scored_answer["question_id"],
        "explanation": {
            "clarity": clarity_exp,
            "relevance": relevance_exp,
            "completeness": completeness_exp,
            "consistency": consistency_exp
        }
    }
