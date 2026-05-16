# screening_ai/optimized_cleaner.py

import re

def advanced_clean(text):
    if not text:
        return ""
    text = text.lower()
    # Remove filler words
    text = re.sub(r"\b(um|uh|like|you know)\b", "", text)
    # Remove repeated words (e.g. "the the" -> "the")
    text = re.sub(r"\b(\w+)( \1\b)+", r"\1", text)
    # Remove noise symbols
    text = re.sub(r"[^\w\s]", "", text)
    # Clean up spacing
    return re.sub(r"\s+", " ", text).strip()
