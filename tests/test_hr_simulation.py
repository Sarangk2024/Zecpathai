# tests/test_hr_simulation.py

from tests.simulate_hr_interview import run_candidate_simulation, run_all_simulations

def test_single_simulation():
    answers = [
        "I am a developer because I built APIs.",
        "First I plan, then I prioritize, and finally execute."
    ]
    durations = [5, 6]
    res = run_candidate_simulation("C_TEST", "technical", "experienced", answers, durations)
    assert res["candidate_id"] == "C_TEST"
    assert "overall_score" in res
    assert "decision" in res
    assert "summary" in res

def test_all_simulations():
    res = run_all_simulations()
    assert "C_CONFIDENT" in res
    assert "C_HESITANT" in res
    assert res["C_CONFIDENT"]["decision"] in ["Strong Hire", "Consider"]
    assert res["C_HESITANT"]["decision"] in ["Consider", "Reject"]
