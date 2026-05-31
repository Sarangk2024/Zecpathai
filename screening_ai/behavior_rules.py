# screening_ai/behavior_rules.py

UNCERTAINTY_WORDS = ["maybe", "not sure", "i think", "probably"]

def detect_uncertainty(text):
    text = text.lower()
    return any(word in text for word in UNCERTAINTY_WORDS)

def detect_contradiction(text):
    text = text.lower()
    if "but" in text or "however" in text:
        return True
    return False
