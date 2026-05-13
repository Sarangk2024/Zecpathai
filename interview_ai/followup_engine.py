# interview_ai/followup_engine.py

# -------------------------------
# Follow-Up Trigger Detection
# -------------------------------
def detect_answer_quality(answer):
    text = answer.lower().strip()
    word_count = len(text.split())
    if not text:
        return "empty"
    if word_count < 4:
        return "too_short"
    if any(phrase in text for phrase in ["not sure", "maybe", "i think"]):
        return "uncertain"
    if word_count < 8:
        return "basic"
    return "good"

# -------------------------------
# Follow-Up Generator
# -------------------------------
def generate_followup(question, answer_quality):
    if answer_quality == "empty":
        return "I didn’t catch that. Could you please answer the question?"
    if answer_quality == "too_short":
        return f"Could you elaborate more on your answer to: '{question}'?"
    if answer_quality == "uncertain":
        return f"You mentioned some uncertainty. Can you clarify your answer to: '{question}'?"
    if answer_quality == "basic":
        return f"Can you provide a real example related to: '{question}'?"
    return None # No follow-up needed
