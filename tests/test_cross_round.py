# tests/test_cross_round.py

from ai_core.cross_round_engine import calculate_final_score, get_weights, aggregation_pipeline
from ai_core.hiring_fit_calculator import calculate_hiring_fit

def test_aggregation():
    # Specifications-requested test structure
    score = calculate_final_score({
        "ats": 70,
        "screening": 70,
        "hr": 70,
        "technical": 70,
        "machine_test": 70
    }, {
        "ats": 0.2,
        "screening": 0.2,
        "hr": 0.2,
        "technical": 0.2,
        "machine_test": 0.2
    })
    assert score == 70

def test_get_weights():
    fresher_weights = get_weights("fresher")
    assert fresher_weights["hr"] == 0.25
    assert fresher_weights["machine_test"] == 0.15

    tech_weights = get_weights("technical")
    assert tech_weights["technical"] == 0.35
    assert tech_weights["screening"] == 0.10

def test_calculate_hiring_fit():
    assert calculate_hiring_fit(88)["fit_category"] == "Excellent Fit"
    assert calculate_hiring_fit(75)["fit_category"] == "Strong Fit"
    assert calculate_hiring_fit(60)["fit_category"] == "Moderate Fit"
    assert calculate_hiring_fit(45)["fit_category"] == "Low Fit"

def test_aggregation_pipeline():
    scores = {
        "ats": 75,
        "screening": 70,
        "hr": 80,
        "technical": 85,
        "machine_test": 78
    }
    result = aggregation_pipeline("C9001", scores, "technical")
    assert result["candidate_id"] == "C9001"
    assert result["final_score"] == 79.5
    assert result["decision"] == "Hire"
    assert result["hiring_fit"]["fit_category"] == "Strong Fit"
