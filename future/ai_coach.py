# future/ai_coach.py

def generate_feedback(scores):
    feedback = []
    if scores.get("communication", 0) < 70:
        feedback.append("Improve communication clarity")
    if scores.get("technical", 0) < 70:
        feedback.append("Strengthen technical fundamentals")
    if scores.get("confidence", 0) < 65:
        feedback.append("Work on confidence and delivery")
    return feedback
