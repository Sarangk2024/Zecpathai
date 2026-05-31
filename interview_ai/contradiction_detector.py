# interview_ai/contradiction_detector.py

def detect_contradiction(text):
    text = text.lower()
    if "but" in text or "however" in text:
        return True
    if "i don't know" in text and "i have experience" in text:
        return True
    return False
