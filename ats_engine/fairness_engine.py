# ats_engine/fairness_engine.py - Fairness, score normalization, and bias-reduction engine for Zecpath AI.

# -------------------------------
# Score Normalization (Min-Max Scaling)
# -------------------------------
def normalize_scores(candidate_scores):
    """
    Apply min-max normalization across candidates in the pool to scale scores to 0-100 range.
    """
    if not candidate_scores:
        return []
        
    scores = [float(c.get("final_score", 0.0)) for c in candidate_scores]
    min_score = min(scores)
    max_score = max(scores)
    
    if max_score == min_score:
        for c in candidate_scores:
            c["normalized_score"] = float(c.get("final_score", 0.0))
        return candidate_scores
        
    for c in candidate_scores:
        final_val = float(c.get("final_score", 0.0))
        normalized = ((final_val - min_score) / (max_score - min_score)) * 100.0
        c["normalized_score"] = round(normalized, 2)
        
    return candidate_scores

# -------------------------------
# Bias Reduction (Masking Sensitive Fields)
# -------------------------------
def mask_sensitive_data(candidate):
    """
    Remove or mask non-essential personal attributes to mitigate unconscious recruitment bias.
    """
    sensitive_fields = ["name", "gender", "age", "photo", "location", "email", "phone"]
    masked = candidate.copy()
    for field in sensitive_fields:
        if field in masked:
            masked[field] = "MASKED"
    return masked

# -------------------------------
# Keyword Bias Reduction
# -------------------------------
def reduce_keyword_bias(skill_score, semantic_score):
    """
    Reduce over-dependence on exact keyword matches by blending keyword matching with semantic matching.
    """
    skill_val = float(skill_score) if skill_score is not None else 0.0
    semantic_val = float(semantic_score) if semantic_score is not None else 0.0
    
    # Blend: 60% semantic similarity + 40% keyword skill score
    adjusted_score = (0.6 * semantic_val) + (0.4 * skill_val)
    return round(adjusted_score, 2)

# -------------------------------
# Fair Candidate Score Generator
# -------------------------------
def generate_fair_score(candidate):
    """
    Generate bias-reduced fair score.
    """
    skill_score = candidate.get("skill_score", 0.0)
    semantic_score = candidate.get("semantic_score", 0.0)
    fair_score = reduce_keyword_bias(skill_score, semantic_score)
    
    # Store in dict
    candidate["fair_score"] = fair_score
    return candidate
