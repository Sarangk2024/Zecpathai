# tests/test_stabilization.py

from ai_core.stable_system import stable_pipeline, safe_score, stable_aggregate
from utils.error_handler import safe_execute
from api.stable_api import api_response
from utils.edge_cases import handle_edge_cases
from utils.conversation_logic import next_step

def test_stable_pipeline():
    # Specifications-requested test structure
    result = stable_pipeline("C1", {"ats": 120, "hr": -10})
    assert result["final_score"] <= 100
    assert result["final_score"] == 50.0 # (100 + 0) / 2 = 50.0. Cleaned is {"ats": 100, "hr": 0} -> average is 50.0.
    # Wait, let's verify math:
    # safe_score(120) = 100
    # safe_score(-10) = 0
    # stable_aggregate({"ats": 120, "hr": -10}) -> average of 100 and 0 = 50.0
    # assert result["final_score"] <= 100

def test_safe_score_types():
    assert safe_score("85.5") == 85.5
    assert safe_score("invalid") == 0
    assert safe_score(None) == 0

def test_safe_execute():
    # Success scenario
    def good_func():
        return 42
    assert safe_execute(good_func, default=0) == 42
    
    # Fault scenario
    def bad_func():
        raise ValueError("Error triggered")
    res = safe_execute(bad_func, default=0)
    assert "error" in res
    assert res["fallback"] == 0

def test_api_response():
    resp_success = api_response(success=True, data={"data_key": 10})
    assert resp_success["success"] is True
    assert resp_success["data"]["data_key"] == 10
    assert resp_success["error"] is None

    resp_error = api_response(success=False, error="Invalid parameter")
    assert resp_error["success"] is False
    assert resp_error["data"] is None
    assert resp_error["error"] == "Invalid parameter"

def test_edge_cases_inputs():
    assert handle_edge_cases("") == "empty"
    assert handle_edge_cases("   ") == "empty"
    assert handle_edge_cases("hello world") == "too_short"
    assert handle_edge_cases("a " * 1005) == "too_long"
    assert handle_edge_cases("Valid answer containing multiple words") == "valid"

def test_conversation_next_step():
    assert next_step("empty", 0) == "ask_again"
    assert next_step("too_short", 1) == "clarify"
    assert next_step("valid", 0) == "continue"
    assert next_step("empty", 3) == "skip_question"
