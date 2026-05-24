# technical_ai/technical_scoring_engine.py

# -------------------------------
# Depth Detection
# -------------------------------
def detect_depth(text):
    keywords = ["because", "architecture", "optimize", "scalable", "tradeoff"]
    count = sum(word in text.lower() for word in keywords)
    if count >= 3:
        return 1.0
    elif count >= 1:
        return 0.7
    return 0.4

# -------------------------------
# Logical Reasoning Score
# -------------------------------
def logical_score(text):
    if "first" in text.lower() and "then" in text.lower():
        return 1.0
    elif len(text.split()) > 10:
        return 0.7
    return 0.4

# -------------------------------
# Real-World Applicability
# -------------------------------
def real_world_score(text):
    if "production" in text.lower() or "real-world" in text.lower():
        return 1.0
    elif "example" in text.lower():
        return 0.7
    return 0.4

# -------------------------------
# Accuracy Score
# -------------------------------
def accuracy_score(is_correct):
    return 1.0 if is_correct else 0.4

# -------------------------------
# Final Technical Score
# -------------------------------
def calculate_technical_score(answer, is_correct=True):
    depth = detect_depth(answer)
    logic = logical_score(answer)
    real_world = real_world_score(answer)
    accuracy = accuracy_score(is_correct)
    
    final = (
        accuracy * 0.35 +
        depth * 0.25 +
        logic * 0.20 +
        real_world * 0.20
    )
    return {
        "technical_score": round(final * 100, 2),
        "breakdown": {
            "accuracy": round(accuracy, 2),
            "depth": round(depth, 2),
            "logic": round(logic, 2),
            "real_world": round(real_world, 2)
        }
    }

# -------------------------------
# Shallow vs Deep Answer Detection
# -------------------------------
def classify_answer_depth(text):
    word_count = len(text.split())
    if word_count > 20 and "because" in text.lower():
        return "deep"
    if word_count > 10:
        return "moderate"
    return "shallow"

# -------------------------------
# Difficulty Normalization
# -------------------------------
def normalize_difficulty(score, difficulty):
    multipliers = {
        "basic": 1.0,
        "intermediate": 1.1,
        "advanced": 1.2
    }
    adjusted = score * multipliers.get(difficulty, 1.0)
    return min(round(adjusted, 2), 100)

# -------------------------------
# Technical Scoring Pipeline
# -------------------------------
def technical_pipeline(answer, difficulty, is_correct=True):
    base_score = calculate_technical_score(answer, is_correct)
    normalized_score = normalize_difficulty(
        base_score["technical_score"],
        difficulty
    )
    return {
        "final_score": normalized_score,
        "details": base_score
    }
