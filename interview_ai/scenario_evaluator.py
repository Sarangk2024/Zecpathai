# interview_ai/scenario_evaluator.py

IDEAL_PATTERNS = {
    "team_conflict": ["communicate", "understand", "resolve"],
    "deadline_pressure": ["prioritize", "plan", "execute"],
    "learning": ["research", "practice", "apply"]
}

def evaluate_scenario(text, scenario_type):
    text = text.lower()
    patterns = IDEAL_PATTERNS.get(scenario_type, [])
    if not patterns:
        return 0.4
    match_count = sum(word in text for word in patterns)
    if match_count == len(patterns):
        return 1.0
    elif match_count > 0:
        return 0.7
    return 0.4
