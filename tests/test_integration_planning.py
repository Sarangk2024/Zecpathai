# tests/test_integration_planning.py

from api.error_handling import retry_request
from api.integration_pipeline import full_integration_pipeline

def test_retry():
    # Specifications-requested test structure
    result = retry_request(lambda: 1)
    assert result == 1

def test_retry_failure():
    def failing_func():
        raise Exception("Connection failed")
        
    result = retry_request(failing_func, retries=2)
    assert "error" in result
    assert result["error"] == "Max retries exceeded"

def test_full_integration_pipeline():
    data = {"candidate_id": "C9001"}
    result = full_integration_pipeline(data)
    assert result["decision"] == "Selected"
    assert result["confidence"] == 85
