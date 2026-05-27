# ai_core/optimized_ai_engine.py

# -------------------------------
# Dynamic Threshold Optimization
# -------------------------------
THRESHOLDS = {
    "selected": 78,  # reduced from 80 for better recall
    "hold": 58      # adjusted for better balance
}

# -------------------------------
# False Positive / Negative Fix
# -------------------------------
def adjust_decision(score, technical, integrity_risk):
    """
    Improve decision accuracy by correcting edge cases
    """
    # Prevent false positives (High score but high cheating risk)
    if score > 80 and integrity_risk == "High Risk":
        return "Hold / Review"
        
    # Prevent false negatives (Low score but exceptionally high technical performance)
    if score < 60 and technical > 85:
        return "Hold / Review"
        
    # Standard decision
    if score >= THRESHOLDS["selected"]:
        return "Selected"
    elif score >= THRESHOLDS["hold"]:
        return "Hold / Review"
    return "Rejected"
