# interview_ai/adaptive_engine.py

# -------------------------------
# Difficulty Adaptation Logic
# -------------------------------
def adapt_question_level(answer_quality, confidence_score):
    # Low-quality answer → simplify
    if answer_quality in ["empty", "too_short"]:
        return "simplify"
    # Medium → ask example
    if answer_quality == "basic":
        return "example"
    # High-quality + confident → deeper probe
    if answer_quality == "good" and confidence_score > 0.7:
        return "advanced"
    return "normal"

# -------------------------------
# Adaptive Question Generator
# -------------------------------
def generate_adaptive_question(base_question, mode):
    if mode == "simplify":
        return f"Let me simplify the question: {base_question}"
    if mode == "example":
        return f"Can you give a real-world example for: {base_question}?"
    if mode == "advanced":
        return f"Can you handle a complex scenario related to: {base_question}?"
    return base_question
