# ai_core/refined_scoring_logic.py

# -------------------------------
# Consistency-Based Score Adjustment
# -------------------------------
def consistency_adjustment(scores):
    values = list(scores.values())
    if not values:
        return 0
    variance = max(values) - min(values)
    # Penalize high inconsistency (large swing across rounds)
    if variance > 30:
        return -5
    # Reward consistent performance across all rounds
    elif variance < 10:
        return +5
    return 0

# -------------------------------
# Final Refined Score
# -------------------------------
def refined_final_score(scores, base_score):
    adjustment = consistency_adjustment(scores)
    return max(min(base_score + adjustment, 100), 0)
