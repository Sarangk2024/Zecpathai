# utils/edge_cases.py

def handle_edge_cases(answer):
    if not answer or len(answer.strip()) == 0:
        return "empty"
    if len(answer.split()) < 3:
        return "too_short"
    if len(answer) > 1000:
        return "too_long"
    return "valid"
