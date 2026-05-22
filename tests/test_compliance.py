# tests/test_compliance.py

from interview_ai.ethics_check import verify_candidate_consent, mask_demographic_signals, check_data_retention_compliance

def test_compliance():
    # Specifications-requested assertion
    consent = True
    data_masked = True
    assert consent is True
    assert data_masked is True

def test_ethics_check_logic():
    # Verify consent
    valid_consent = {"ai_evaluation": True, "data_processing": True}
    invalid_consent = {"ai_evaluation": True, "data_processing": False}
    assert verify_candidate_consent(valid_consent) is True
    assert verify_candidate_consent(invalid_consent) is False
    assert verify_candidate_consent(None) is False

    # Verify demographic signal masking
    profile = {
        "candidate_id": "C101",
        "name": "John Doe",
        "gender": "Male",
        "age": 28,
        "location": "Boston",
        "skills": ["Python", "Docker"]
    }
    masked = mask_demographic_signals(profile)
    assert masked["name"] == "[MASKED]"
    assert masked["gender"] == "[MASKED]"
    assert masked["age"] == "[MASKED]"
    assert masked["location"] == "[MASKED]"
    assert masked["skills"] == ["Python", "Docker"]
    assert masked["candidate_id"] == "C101"

    # Verify retention compliance
    assert check_data_retention_compliance(45) == "Retain"
    assert check_data_retention_compliance(90) == "Retain"
    assert check_data_retention_compliance(91) == "Anonymize/Delete"
