# screening_ai/error_handling.py

def detect_issue(answer):
    if not answer or len(answer.strip()) == 0:
        return "silence"
    if len(answer.split()) < 2:
        return "confusion"
    # Check repeating pattern (if unique words are less than half of total words)
    words = answer.split()
    if len(set(words)) < len(words) / 2:
        return "repeat"
    return "valid"

def handle_response(state_machine, answer):
    issue = detect_issue(answer)
    if issue == "silence":
        state_machine.handle_silence()
    elif issue == "confusion":
        state_machine.handle_confusion()
    elif issue == "repeat":
        state_machine.handle_repeat()
    else:
        state_machine.next()

RETRY_MESSAGES = {
    "silence": "Sorry, I didn’t hear anything. Could you please respond?",
    "confusion": "Let me clarify the question for you.",
    "repeat": "Could you provide more details?"
}
