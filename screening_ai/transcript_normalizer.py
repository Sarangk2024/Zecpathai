# screening_ai/transcript_normalizer.py - Transcript normalizations and cleaning rules.

import re

def normalize_transcript(text):
    if not text:
        return ""
        
    # Convert to lowercase
    text = text.lower()
    
    # Remove filler words: "um", "uh", "like", "you know"
    fillers = ["um", "uh", "like", "you know"]
    for f in fillers:
        # Match word boundaries to avoid stripping letters from normal words
        text = re.sub(rf"\b{f}\b", "", text, flags=re.IGNORECASE)
        
    # Remove extra spaces (multiple spaces -> single space)
    text = re.sub(r"\s+", " ", text)
    
    return text.strip()

def process_transcript(raw_answers):
    processed = []
    for ans in raw_answers:
        normalized = normalize_transcript(ans.get("text", ""))
        processed.append({
            "question_id": ans.get("question_id"),
            "answer_text": normalized,
            "confidence_score": ans.get("confidence", 0.9)
        })
    return processed
