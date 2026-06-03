# tests/test_final_polish.py

from ai_core.final_production_system import production_pipeline, normalize_score, smooth_scores
from utils.final_error_handler import safe_run

def test_production():
    # Specifications-requested test structure
    result = production_pipeline("C1", {"ats": 90, "hr": 80})
    assert result["decision"] in ["Selected", "Hold / Review", "Rejected"]

def test_normalize_score():
    assert normalize_score(125.0) == 100.0
    assert normalize_score(-15.0) == 0.0
    assert normalize_score("invalid") == 0.0
    assert normalize_score(82.5) == 82.5

def test_smooth_scores():
    scores = {"ats": 100, "technical": 50}
    # average is 75
    # ats smoothed: 100 * 0.7 + 75 * 0.3 = 70 + 22.5 = 92.5
    # technical smoothed: 50 * 0.7 + 75 * 0.3 = 35 + 22.5 = 57.5
    smoothed = smooth_scores(scores)
    assert smoothed["ats"] == 92.5
    assert smoothed["technical"] == 57.5

def test_safe_run():
    # Success scenario
    assert safe_run(lambda: 10, fallback=0) == 10
    
    # Error scenario
    res = safe_run(lambda: 1/0, fallback=0.0)
    assert res["status"] == "handled"
    assert "division by zero" in res["error"]
    assert res["fallback"] == 0.0
