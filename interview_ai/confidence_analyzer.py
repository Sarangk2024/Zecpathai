# interview_ai/confidence_analyzer.py

# -------------------------------
# Hesitation / Uncertainty Words
# -------------------------------
HESITATION_WORDS = ["um", "uh", "hmm"]
UNCERTAINTY_PHRASES = ["not sure", "maybe", "i think", "probably"]

# -------------------------------
# Repeated Words Detection
# -------------------------------
def repeated_word_score(text):
    words = text.lower().split()
    if not words:
        return 1.0
    repeats = len(words) - len(set(words))
    ratio = repeats / (len(words) + 1)
    if ratio < 0.1:
        return 1.0
    elif ratio < 0.3:
        return 0.7
    return 0.4

# -------------------------------
# Hesitation Score
# -------------------------------
def hesitation_score(text):
    text = text.lower()
    count = sum(text.count(word) for word in HESITATION_WORDS)
    return max(0.0, 1.0 - min(count * 0.2, 1.0))

# -------------------------------
# Uncertainty Score
# -------------------------------
def uncertainty_score(text):
    text = text.lower()
    count = sum(phrase in text for phrase in UNCERTAINTY_PHRASES)
    if count == 0:
        return 1.0
    elif count == 1:
        return 0.6
    return 0.3

# -------------------------------
# Pause Score (simulated via length)
# -------------------------------
def pause_score(duration, word_count):
    if word_count == 0 or duration == 0:
        return 0.0
    wps = word_count / duration
    if 1.5 <= wps <= 3:
        return 1.0
    elif 1.0 <= wps < 1.5 or 3 < wps <= 4:
        return 0.7
    return 0.4

# -------------------------------
# Final Confidence Score
# -------------------------------
def calculate_confidence(text, duration):
    words = len(text.split())
    repeat = repeated_word_score(text)
    hesitation = hesitation_score(text)
    uncertainty = uncertainty_score(text)
    pause = pause_score(duration, words)
    
    score = (
        repeat * 0.25 +
        hesitation * 0.25 +
        uncertainty * 0.25 +
        pause * 0.25
    )
    
    return {
        "confidence_score": round(score * 100, 2),
        "signals": {
            "repeat": round(repeat, 2),
            "hesitation": round(hesitation, 2),
            "uncertainty": round(uncertainty, 2),
            "pause": round(pause, 2)
        }
    }
