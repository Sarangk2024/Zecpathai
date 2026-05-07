# tests/test_ranking_engine.py - Unit tests for candidate ranking and shortlisting engine.

from ats_engine.ranking_engine import (
    rank_candidates, classify_candidate, 
    apply_shortlisting, get_top_candidates, ranking_pipeline
)

def test_ranking():
    candidates = [
        {"candidate_id": "C1", "final_score": 50},
        {"candidate_id": "C2", "final_score": 80}
    ]
    ranked = rank_candidates(candidates)
    assert ranked[0]["candidate_id"] == "C2"
    assert ranked[0]["rank"] == 1
    assert ranked[1]["candidate_id"] == "C1"
    assert ranked[1]["rank"] == 2

def test_classify_candidate():
    assert classify_candidate(80) == "Shortlisted"
    assert classify_candidate(60) == "Review"
    assert classify_candidate(40) == "Rejected"

def test_ranking_pipeline():
    candidates = [
        {"candidate_id": "C1", "final_score": 88},
        {"candidate_id": "C2", "final_score": 72},
        {"candidate_id": "C3", "final_score": 45},
        {"candidate_id": "C4", "final_score": 80}
    ]
    result = ranking_pipeline(candidates)
    assert len(result["ranked_list"]) == 4
    assert result["ranked_list"][0]["candidate_id"] == "C1"
    assert result["ranked_list"][0]["status"] == "Shortlisted"
    assert result["ranked_list"][1]["candidate_id"] == "C4"
    assert result["ranked_list"][1]["status"] == "Shortlisted"
    assert result["ranked_list"][2]["candidate_id"] == "C2"
    assert result["ranked_list"][2]["status"] == "Review"
    assert result["ranked_list"][3]["candidate_id"] == "C3"
    assert result["ranked_list"][3]["status"] == "Rejected"
