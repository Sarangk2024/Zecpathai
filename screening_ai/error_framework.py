# screening_ai/error_framework.py

ERROR_RESPONSES = {
    "missing": "I didn’t receive your response. Could you please answer?",
    "poor_audio": "The audio is unclear. Could you please repeat?",
    "unclear": "Can you please explain that more clearly?",
    "language_mix": "Would you prefer to continue in another language?",
    "incomplete": "Could you provide more details?",
    "fallback": "Let’s move to the next question."
}

def get_error_response(issue):
    return ERROR_RESPONSES.get(issue, ERROR_RESPONSES["fallback"])

def fallback_strategy(issue, retry_count):
    if retry_count >= 2:
        return "skip_question"
    if issue in ["missing", "poor_audio"]:
        return "retry"
    if issue == "language_mix":
        return "switch_language"
    return "clarify"
