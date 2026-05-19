# tests/test_aptitude.py

from interview_ai.aptitude_scoring import calculate_aptitude_score, detect_structure
from interview_ai.scenario_evaluator import evaluate_scenario
from interview_ai.aptitude_pipeline import aptitude_pipeline

def test_aptitude():
    result = calculate_aptitude_score("First I analyze then solve")
    assert result["aptitude_score"] > 0

def test_structure_scoring():
    # first, then, next, finally, because, therefore
    assert detect_structure("First I will do A. Then B. Finally C.") == 1.0
    assert detect_structure("First I will do A.") == 0.7
    assert detect_structure("No structure tags here.") == 0.4

def test_scenario_match():
    # prioritize, plan, execute
    ans_good = "I will prioritize tasks, establish a plan, and execute efficiently."
    assert evaluate_scenario(ans_good, "deadline_pressure") == 1.0
    assert evaluate_scenario("I will plan the task.", "deadline_pressure") == 0.7
    assert evaluate_scenario("Nothing matching.", "deadline_pressure") == 0.4

def test_pipeline():
    ans = "First I will analyze the problem to prioritize and plan the solution, then execute it, and finally review."
    res = aptitude_pipeline(ans, "deadline_pressure")
    assert res["aptitude_score"] == 100.0
    assert res["scenario_score"] == 1.0
