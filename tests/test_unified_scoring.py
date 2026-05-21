# tests/test_unified_scoring.py

from ai_core.unified_scoring_engine import calculate_unified_score, get_weights, unified_scoring_pipeline
from ai_core.hiring_fit import calculate_hiring_fit

def test_unified():
    result = calculate_unified_score(80, 70, 85, {
        "ats": 0.3,
        "screening": 0.3,
        "hr": 0.4
    })
    assert result > 0
    assert result == 79.0

def test_fit_calculation():
    assert calculate_hiring_fit(85)["fit_category"] == "Excellent Fit"
    assert calculate_hiring_fit(75)["fit_category"] == "Good Fit"
    assert calculate_hiring_fit(60)["fit_category"] == "Moderate Fit"
    assert calculate_hiring_fit(40)["fit_category"] == "Low Fit"

def test_weight_profiles():
    assert get_weights("fresher")["screening"] == 0.35
    assert get_weights("experienced")["ats"] == 0.35
    assert get_weights("technical")["ats"] == 0.40
    assert get_weights("non_technical")["hr"] == 0.50

def test_unified_pipeline():
    res = unified_scoring_pipeline("C500", 78, 72, 85, "technical")
    assert res["candidate_id"] == "C500"
    assert res["final_score"] == 78.3 # 78*0.4 + 72*0.3 + 85*0.3 = 31.2 + 21.6 + 25.5 = 78.3
    assert res["decision"] == "Hire"
    assert res["fit"]["fit_category"] == "Good Fit"
