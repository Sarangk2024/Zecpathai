# tests/test_release_ready.py

from ai_core.release_ready_system import release_pipeline, safe_value, final_aggregate

def test_release():
    # Specifications-requested test structure
    result = release_pipeline("C1", {"ats": 120, "hr": -10})
    assert result["final_score"] >= 0
    assert result["scores"]["ats"] == 100.0
    assert result["scores"]["hr"] == 0.0
    assert result["final_score"] == 50.0

def test_safe_value():
    assert safe_value("90.5") == 90.5
    assert safe_value(-5.0) == 0.0
    assert safe_value(115.0) == 100.0
    assert safe_value("invalid", default=10.0) == 10.0

def test_final_aggregate():
    scores = {"ats": 80, "hr": 90, "technical": 70}
    assert final_aggregate(scores) == 80.0
    assert final_aggregate({}) == 0.0

def test_release_pipeline_details():
    res = release_pipeline("C999", {"ats": 85, "technical": 95, "hr": 70})
    assert res["candidate_id"] == "C999"
    assert res["final_score"] == 83.33
    assert res["decision"] == "Selected"
    assert res["status"] == "release_ready"
