# screening_ai/answer_engine.py - Intent classification and entity understanding engine.

import re

# -------------------------------
# Intent Keywords Mapping
# -------------------------------
INTENT_MAP = {
    "introduction": ["introduce", "about myself", "background", "my name"],
    "experience": ["experience", "years", "worked", "role", "career"],
    "skills": ["skills", "technologies", "tools", "languages", "knows"],
    "salary": ["salary", "ctc", "pay", "expectation", "package"],
    "availability": ["notice period", "available", "join", "weeks", "immediate"]
}

# -------------------------------
# Intent Classification
# -------------------------------
def classify_intent(text):
    if not text:
        return "unknown"
    text_lower = text.lower()
    for intent, keywords in INTENT_MAP.items():
        for word in keywords:
            if word in text_lower:
                return intent
    return "unknown"

# -------------------------------
# Skill Extraction (Simple)
# -------------------------------
SKILL_DB = ["python", "java", "django", "react", "sql", "cnc", "fitting", "milling"]

def extract_skills(text):
    if not text:
        return []
    text = text.lower()
    return [skill for skill in SKILL_DB if skill in text]

# -------------------------------
# Experience Extraction
# -------------------------------
def extract_experience(text):
    if not text:
        return 0
    match = re.search(r"(\d+)\s*(years|year)", text.lower())
    return int(match.group(1)) if match else 0

# -------------------------------
# Salary Extraction
# -------------------------------
def extract_salary(text):
    if not text:
        return None
    # Matches patterns like '5 lpa', '6 lakhs', '80k', etc.
    match = re.search(r"(\d+)\s*(lpa|lakhs|lakh|k)", text.lower())
    return match.group(0) if match else None

# -------------------------------
# Availability Detection
# -------------------------------
def extract_availability(text):
    if not text:
        return "Unknown"
    text_lower = text.lower()
    if "immediate" in text_lower or "immediately" in text_lower or "no notice" in text_lower:
        return "Immediate"
    elif "notice" in text_lower or "week" in text_lower or "month" in text_lower:
        return "Notice Period"
    return "Unknown"

# -------------------------------
# Off-topic Detection
# -------------------------------
def is_off_topic(intent):
    return intent == "unknown"

# -------------------------------
# Vague Answer Detection
# -------------------------------
def is_vague(text):
    if not text:
        return True
    vague_words = ["maybe", "not sure", "don't know", "depends", "probably"]
    return any(word in text.lower() for word in vague_words)

# -------------------------------
# Missing Answer Detection
# -------------------------------
def detect_missing_answer(text):
    return not text or len(text.strip()) < 3

# -------------------------------
# Main Answer Processing
# -------------------------------
def process_answer(question_id, answer_text):
    intent = classify_intent(answer_text)
    
    # Check for empty/missing answers
    is_missing = detect_missing_answer(answer_text)
    
    structured = {
        "question_id": question_id,
        "original_text": answer_text,
        "intent": intent if not is_missing else "missing",
        "skills": extract_skills(answer_text) if not is_missing else [],
        "experience_years": extract_experience(answer_text) if not is_missing else 0,
        "salary": extract_salary(answer_text) if not is_missing else None,
        "availability": extract_availability(answer_text) if not is_missing else "Unknown",
        "off_topic": is_off_topic(intent) if not is_missing else False,
        "is_vague": is_vague(answer_text) if not is_missing else False
    }
    return structured

# -------------------------------
# Batch Answer Processing
# -------------------------------
def process_answers_batch(answers):
    results = []
    for ans in answers:
        result = process_answer(ans.get("question_id"), ans.get("text", ""))
        results.append(result)
    return results
