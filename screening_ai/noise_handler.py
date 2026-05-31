# screening_ai/noise_handler.py

import re

def clean_noise(text):
    # Remove background noise markers
    text = re.sub(r"\[.*?\]", "", text)
    # Remove repeated characters (3 or more)
    text = re.sub(r"(.)\1{2,}", r"\1", text)
    return text.strip()

def detect_language_mix(text):
    local_words = ["hai", "enna", "chetta", "bhai"]
    for word in local_words:
        if word in text.lower():
            return True
    return False
