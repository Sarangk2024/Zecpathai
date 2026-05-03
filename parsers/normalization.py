# parsers/normalization.py - Text normalization and heading standardization module for Zecpath AI.

import re

# -------------------------------
# Standard Resume Normalization
# -------------------------------
def normalize_resume_text(text):
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters
    text = re.sub(r"[^a-z0-9\s\.\,\-]", "", text)
    
    # Normalize spaces
    text = re.sub(r"\s+", " ", text)
    
    # Standardize common resume headings
    replacements = {
        "professional experience": "experience",
        "work experience": "experience",
        "academic background": "education",
        "academic history": "education",
        "skill set": "skills",
        "technical skills": "skills",
        "projects descriptions": "projects",
        "projects description": "projects",
        "project details": "projects",
        "personal projects": "projects"
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
        
    return text.strip()
