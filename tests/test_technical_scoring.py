# tests/test_technical_scoring.py

from technical_ai.technical_scoring_engine import (
    calculate_technical_score,
    detect_depth,
    logical_score,
    real_world_score,
    classify_answer_depth,
    normalize_difficulty,
    technical_pipeline
)

def test_technical():
    # Specifications-requested test structure
    result = calculate_technical_score("This is a correct answer", True)
    assert result["technical_score"] > 0

def test_detect_depth():
    # 3 keywords -> 1.0
    text_deep = "because we need a scalable architecture"
    assert detect_depth(text_deep) == 1.0
    # 1 keyword -> 0.7
    text_mod = "we optimize code"
    assert detect_depth(text_mod) == 0.7
    # 0 keyword -> 0.4
    text_shallow = "I wrote python code"
    assert detect_depth(text_shallow) == 0.4

def test_logical_score():
    assert logical_score("First do this, then do that") == 1.0
    assert logical_score("This is a long string with more than ten words in it") == 0.7
    assert logical_score("short text") == 0.4

def test_real_world_score():
    assert real_world_score("This goes into production") == 1.0
    assert real_world_score("For example React usecase") == 0.7
    assert real_world_score("No practical scenario") == 0.4

def test_classify_answer_depth():
    assert classify_answer_depth("We use this architecture because we need to keep the database scaling under heavy load in production systems and avoid timeouts.") == "deep"
    assert classify_answer_depth("This is a medium response containing more than ten words now") == "moderate"
    assert classify_answer_depth("short") == "shallow"

def test_normalize_difficulty():
    assert normalize_difficulty(50.0, "basic") == 50.0
    assert normalize_difficulty(50.0, "intermediate") == 55.0
    assert normalize_difficulty(50.0, "advanced") == 60.0
    assert normalize_difficulty(90.0, "advanced") == 100.0 # max out at 100

def test_technical_pipeline():
    answer = "First I design architecture, then optimize for scalability because real-world systems need performance."
    pipe = technical_pipeline(answer, "advanced", True)
    assert pipe["final_score"] > 0
    assert "details" in pipe
