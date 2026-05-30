# tests/test_performance_tuning.py

from ai_core.performance_optimized import fast_decision, cached_ats_score, batch_resume_processing
from api.optimized_api import optimized_response
from utils.memory_optimizer import memory_efficient_processing
from tests.load_test import simulate_load

def test_performance():
    # Specifications-requested test structure
    result = fast_decision(80)
    assert result == "Selected"
    assert fast_decision(60) == "Hold / Review"
    assert fast_decision(40) == "Rejected"

def test_caching():
    score1 = cached_ats_score("candidate_a_hash")
    score2 = cached_ats_score("candidate_a_hash")
    assert score1 == score2

def test_batch_processing():
    resumes = [10, 20, 30]
    func = lambda x: x + 5
    results = batch_resume_processing(resumes, func)
    assert results == [15, 25, 35]

def test_optimized_response():
    resp = optimized_response("payload_data")
    assert resp["result"]["data"] == "payload_data"
    assert "latency_ms" in resp

def test_memory_optimization():
    stream = range(5)
    generator = memory_efficient_processing(stream)
    results = list(generator)
    assert results == [0, 2, 4, 6, 8]

def test_load_simulation():
    res = simulate_load(100)
    assert "avg_response" in res
    assert "max_response" in res
    assert 0.5 <= res["avg_response"] <= 1.5
