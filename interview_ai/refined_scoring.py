# interview_ai/refined_scoring.py

def normalize_scores(scores):
    min_s = min(scores) if scores else 0
    max_s = max(scores) if scores else 1
    if max_s == min_s:
        # If all scores are the same, normalize to them directly or prevent division by zero
        return [float(s) for s in scores]
    return [(s - min_s) / (max_s - min_s) * 100 for s in scores]

def reduce_bias(score, confidence):
    # Reduce penalty for low confidence slightly
    adjusted = score * 0.9 + confidence * 0.1
    return round(adjusted, 2)

def refined_score_pipeline(scores, confidence_scores):
    normalized = normalize_scores(scores)
    final_scores = []
    for s, c in zip(normalized, confidence_scores):
        final_scores.append(reduce_bias(s, c))
    return final_scores
