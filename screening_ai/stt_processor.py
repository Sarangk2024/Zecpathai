# screening_ai/stt_processor.py - Speech-to-Text Integration and Cleaning layer.

import re

# -------------------------------
# Simulated STT Integration Layer
# -------------------------------
def speech_to_text(audio_input):
    """
    Simulated STT output (replace with real API: Whisper, Google STT, etc.)
    """
    # Simple fallback check
    if not audio_input:
        return {"text": "", "confidence": 0.0}
    return {
        "text": audio_input,
        "confidence": 0.92
    }

# -------------------------------
# Filler Word Removal
# -------------------------------
FILLER_WORDS = ["um", "uh", "like", "you know", "hmm"]

def remove_fillers(text):
    if not text:
        return ""
    for word in FILLER_WORDS:
        # Standardize matching boundary
        text = re.sub(rf"\b{word}\b", "", text, flags=re.IGNORECASE)
    return text

# -------------------------------
# Punctuation Correction
# -------------------------------
def fix_punctuation(text):
    if not text:
        return ""
    text = text.strip()
    
    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]
        
    # Add period if missing and does not end with standard punctuation
    if text and not text.endswith((".", "!", "?")):
        text += "."
    return text

# -------------------------------
# Normalize Case & Spacing
# -------------------------------
def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------------
# Handle Interrupted Speech
# -------------------------------
def handle_interruptions(text):
    if not text:
        return ""
    # Remove repeated characters (3 or more)
    text = re.sub(r"(.)\1{2,}", r"\1", text)
    return text

# -------------------------------
# Silence Detection
# -------------------------------
def detect_silence(text):
    if not text or len(text.strip()) < 2:
        return True
    return False

# -------------------------------
# Full Transcript Cleaning Pipeline
# -------------------------------
def clean_transcript(audio_input):
    stt_result = speech_to_text(audio_input)
    raw_text = stt_result["text"]
    confidence = stt_result["confidence"]
    
    if detect_silence(raw_text):
        return {
            "clean_text": "",
            "confidence": confidence,
            "status": "silence_detected"
        }
        
    text = remove_fillers(raw_text)
    text = handle_interruptions(text)
    text = normalize_text(text)
    text = fix_punctuation(text)
    
    # Clean double spaces created by filler removal
    text = re.sub(r"\s+", " ", text).strip()
    text = fix_punctuation(text) # Recapitalize if normalizer modified prefix
    
    return {
        "clean_text": text,
        "confidence": confidence,
        "status": "processed"
    }
