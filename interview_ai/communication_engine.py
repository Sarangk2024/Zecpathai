# interview_ai/communication_engine.py

import re

# -------------------------------
# Filler Words
# -------------------------------
FILLER_WORDS = ["um", "uh", "like", "you know", "actually", "basically"]

# -------------------------------
# Fluency Score (sentence continuity)
# -------------------------------
def score_fluency(text):
    sentences = re.split(r'[.!?]', text)
    valid_sentences = [s.strip() for s in sentences if len(s.split()) > 3]
    if len(valid_sentences) >= 2:
        return 1.0
    elif len(valid_sentences) == 1:
        return 0.6
    return 0.3

# -------------------------------
# Grammar Score (basic heuristic)
# -------------------------------
def score_grammar(text):
    stripped = text.strip()
    if not stripped:
        return 0.4
    if stripped[0].isupper() and stripped.endswith(('.', '?', '!')):
        return 1.0
    elif len(stripped.split()) > 5:
        return 0.7
    return 0.4

# -------------------------------
# Vocabulary Score
# -------------------------------
def score_vocabulary(text):
    words = text.lower().split()
    if not words:
        return 0.4
    unique_words = set(words)
    if len(unique_words) / (len(words) + 1) > 0.6:
        return 1.0
    elif len(unique_words) > 5:
        return 0.7
    return 0.4

# -------------------------------
# Clarity Score
# -------------------------------
def score_clarity(text):
    length = len(text.split())
    if length > 12:
        return 1.0
    elif length > 6:
        return 0.7
    return 0.4

# -------------------------------
# Filler Word Penalty
# -------------------------------
def filler_penalty(text):
    text = text.lower()
    count = sum(text.count(word) for word in FILLER_WORDS)
    penalty = min(count * 0.1, 0.5)
    return penalty

# -------------------------------
# Structure Score
# -------------------------------
def score_structure(text):
    if "because" in text.lower() or "for example" in text.lower():
        return 1.0
    elif len(text.split()) > 6:
        return 0.7
    return 0.4

# -------------------------------
# Final Communication Score
# -------------------------------
def calculate_communication_score(text):
    fluency = score_fluency(text)
    grammar = score_grammar(text)
    vocab = score_vocabulary(text)
    clarity = score_clarity(text)
    structure = score_structure(text)
    penalty = filler_penalty(text)
    
    score = (
        fluency * 0.2 +
        grammar * 0.2 +
        vocab * 0.2 +
        clarity * 0.2 +
        structure * 0.2
    )
    score = max(score - penalty, 0)
    
    return {
        "communication_score": round(score * 100, 2),
        "breakdown": {
            "fluency": round(fluency, 2),
            "grammar": round(grammar, 2),
            "vocabulary": round(vocab, 2),
            "clarity": round(clarity, 2),
            "structure": round(structure, 2),
            "penalty": round(penalty, 2)
        }
    }
