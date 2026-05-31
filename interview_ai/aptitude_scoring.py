# interview_ai/aptitude_scoring.py

# -------------------------------
# Logical Structure Detection
# -------------------------------
def detect_structure(text):
    keywords = ["first", "then", "next", "finally", "because", "therefore"]
    count = sum(word in text.lower() for word in keywords)
    if count >= 3:
        return 1.0
    elif count >= 1:
        return 0.7
    return 0.4

# -------------------------------
# Problem-Solving Clarity
# -------------------------------
def problem_solving_score(text):
    if "solution" in text.lower() or "approach" in text.lower():
        return 1.0
    elif len(text.split()) > 10:
        return 0.7
    return 0.4

# -------------------------------
# Decision Quality
# -------------------------------
def decision_score(text):
    if "consider" in text.lower() or "analyze" in text.lower():
        return 1.0
    elif "try" in text.lower():
        return 0.7
    return 0.4

# -------------------------------
# Final Aptitude Score
# -------------------------------
def calculate_aptitude_score(text):
    structure = detect_structure(text)
    problem = problem_solving_score(text)
    decision = decision_score(text)
    
    final = (
        structure * 0.35 +
        problem * 0.35 +
        decision * 0.30
    )
    
    return {
        "aptitude_score": round(final * 100, 2),
        "breakdown": {
            "structure": round(structure, 2),
            "problem_solving": round(problem, 2),
            "decision_making": round(decision, 2)
        }
    }
