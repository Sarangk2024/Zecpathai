# technical_ai/difficulty_engine.py

def adjust_difficulty(current_level, answer_quality):
    levels = ["basic", "intermediate", "advanced"]
    try:
        idx = levels.index(current_level)
    except ValueError:
        return "basic"
        
    if answer_quality == "good" and idx < 2:
        return levels[idx + 1]
    if answer_quality == "poor" and idx > 0:
        return levels[idx - 1]
    return current_level
