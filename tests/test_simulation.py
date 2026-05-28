# tests/test_simulation.py

from tests.full_simulation import run_full_simulation

def test_simulation():
    # Specifications-requested test structure
    results = run_full_simulation(10)
    assert len(results) == 10
    
    for r in results:
        assert "scores" in r
        assert "decision" in r
        assert "ats" in r["scores"]
        assert "screening" in r["scores"]
        assert "hr" in r["scores"]
        assert "technical" in r["scores"]
        assert "machine_test" in r["scores"]
        assert r["decision"] in ["Selected", "Rejected"]
