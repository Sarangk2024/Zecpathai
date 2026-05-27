# tests/test_optimization_refinement.py

from ai_core.optimized_ai_engine import adjust_decision
from ai_core.refined_scoring_logic import consistency_adjustment, refined_final_score
from nlp.intent_refinement import refined_intent_detection

def test_optimization():
    # Specifications-requested test structure
    decision = adjust_decision(85, 90, "High Risk")
    assert decision == "Hold / Review"

def test_decision_edge_cases():
    # Standard decision
    assert adjust_decision(80, 70, "Low Risk") == "Selected"
    assert adjust_decision(65, 60, "Low Risk") == "Hold / Review"
    assert adjust_decision(50, 50, "Low Risk") == "Rejected"
    
    # False Negative correction: score < 60, but technical > 85 -> Hold / Review
    assert adjust_decision(55, 90, "Low Risk") == "Hold / Review"
    
    # False Positive correction: score > 80, but high integrity risk -> Hold / Review
    assert adjust_decision(85, 80, "High Risk") == "Hold / Review"

def test_consistency_scoring():
    # High variance (>30) -> penalty of -5
    scores_inconsistent = {"ats": 90, "technical": 40, "hr": 85}
    assert consistency_adjustment(scores_inconsistent) == -5
    assert refined_final_score(scores_inconsistent, 72) == 67

    # Low variance (<10) -> bonus of +5
    scores_consistent = {"ats": 82, "technical": 80, "hr": 85}
    assert consistency_adjustment(scores_consistent) == 5
    assert refined_final_score(scores_consistent, 82) == 87

    # Normal variance -> no change
    scores_normal = {"ats": 80, "technical": 65, "hr": 75}
    assert consistency_adjustment(scores_normal) == 0
    assert refined_final_score(scores_normal, 73) == 73

def test_refined_intent_detection():
    assert refined_intent_detection("I implemented a Python pipeline") == "experience"
    assert refined_intent_detection("I completed a B.Tech degree") == "education"
    assert refined_intent_detection("I will study Kubernetes in the future") == "future_intent"
    assert refined_intent_detection("Hello world response") == "generic"
