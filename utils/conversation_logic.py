# utils/conversation_logic.py

def next_step(answer_quality, retry_count):
    if retry_count > 2:
        return "skip_question"
    if answer_quality == "empty":
        return "ask_again"
    if answer_quality == "too_short":
        return "clarify"
    return "continue"
