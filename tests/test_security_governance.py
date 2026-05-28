# tests/test_security_governance.py

from security.access_control import has_access
from security.audit_log import log_event
from security.encryption import encrypt_data, decrypt_data

def test_access():
    # Specifications-requested test structure
    assert has_access("admin", "delete") == True
    assert has_access("viewer", "write") == False

def test_has_access_details():
    assert has_access("admin", "read") == True
    assert has_access("recruiter", "write") == True
    assert has_access("recruiter", "delete") == False
    assert has_access("viewer", "read") == True

def test_audit_log():
    log = log_event("decision_generated", "C15001", {"decision": "Selected", "score": 82})
    assert log["event_type"] == "decision_generated"
    assert log["candidate_id"] == "C15001"
    assert log["data"]["decision"] == "Selected"
    assert "timestamp" in log

def test_encryption():
    secret_text = "Highly confidential data profile details"
    encrypted = encrypt_data(secret_text)
    assert encrypted != secret_text
    
    decrypted = decrypt_data(encrypted)
    assert decrypted == secret_text
