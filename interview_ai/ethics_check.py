# interview_ai/ethics_check.py

import re

def verify_candidate_consent(consent_object):
    if not consent_object:
        return False
    # Check if candidate explicitly agreed to AI evaluation and data processing
    return consent_object.get("ai_evaluation", False) and consent_object.get("data_processing", False)

def mask_demographic_signals(candidate_profile):
    """
    Remove demographic bias signals (like name, gender, age, location, etc.)
    before passing candidate data to screening and evaluation algorithms.
    """
    masked_profile = candidate_profile.copy()
    
    # Fields to mask/remove
    sensitive_fields = ["name", "gender", "age", "location", "religion", "caste"]
    for field in sensitive_fields:
        if field in masked_profile:
            masked_profile[field] = "[MASKED]"
            
    return masked_profile

def check_data_retention_compliance(days_stored):
    """
    Candidate data stored for more than 90 days must be anonymized or deleted.
    """
    if days_stored > 90:
        return "Anonymize/Delete"
    return "Retain"
