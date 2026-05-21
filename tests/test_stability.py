# tests/test_stability.py

from interview_ai.stable_hr_ai import stable_hr_evaluation, smooth_score, stable_decision
from interview_ai.refined_scoring import refined_score_pipeline, normalize_scores, reduce_bias
from interview_ai.followup_stability import stable_followup
from screening_ai.optimized_cleaner import advanced_clean
from utils.batch_processing import batch_process

def test_stability():
    # Basic test requested by specifications
    result = stable_hr_evaluation([50, 60, 90, 30])
    assert result["stable_score"] > 0

def test_smooth_score():
    # Outliers (deviating more than 20 from average) should be removed
    # average of [50, 60, 90, 30] is 57.5.
    # Deviation from 57.5: 50 (7.5), 60 (2.5), 90 (32.5 - outlier!), 30 (27.5 - outlier!).
    # So filtered: [50, 60] -> average is 55.0
    scores = [50, 60, 90, 30]
    smoothed = smooth_score(scores)
    assert smoothed == 55.0

    # Test empty input
    assert smooth_score([]) == 0

def test_stable_decision():
    assert stable_decision(80) == "Hire"
    assert stable_decision(75) == "Hire"
    assert stable_decision(70) == "Consider"
    assert stable_decision(55) == "Consider"
    assert stable_decision(50) == "Reject"

def test_normalize_scores():
    scores = [10, 20, 30]
    normalized = normalize_scores(scores)
    assert normalized == [0.0, 50.0, 100.0]
    
    # Single element or identical elements
    assert normalize_scores([50, 50]) == [50.0, 50.0]
    assert normalize_scores([]) == []

def test_reduce_bias():
    # score * 0.9 + confidence * 0.1
    assert reduce_bias(80, 90) == 81.0
    assert reduce_bias(50, 10) == 46.0

def test_refined_score_pipeline():
    scores = [10, 20, 30]
    confidences = [80, 90, 100]
    # normalized: [0, 50, 100]
    # 0*0.9 + 80*0.1 = 8.0
    # 50*0.9 + 90*0.1 = 45.0 + 9.0 = 54.0
    # 100*0.9 + 100*0.1 = 90.0 + 10.0 = 100.0
    refined = refined_score_pipeline(scores, confidences)
    assert refined == [8.0, 54.0, 100.0]

def test_stable_followup():
    assert stable_followup("empty", 0) == "clarify"
    assert stable_followup("too_short", 1) == "clarify"
    assert stable_followup("uncertain", 1) == "simplify"
    assert stable_followup("uncertain", 2) == "skip"
    assert stable_followup("perfect", 0) == "continue"

def test_advanced_clean():
    # um, uh, like, you know removal, deduplication, symbol removal, extra space collapse
    raw_text = "Um, like, I think Python is is really, you know, good."
    cleaned = advanced_clean(raw_text)
    assert cleaned == "i think python is really good"

def test_batch_process():
    data = ["Um, uh, hello", "world like"]
    cleaned_batch = batch_process(data, advanced_clean)
    assert cleaned_batch == ["hello", "world"]
