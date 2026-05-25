# tests/test_machine_test.py

from machine_test.evaluation_logic import (
    calculate_task_score,
    correctness_score,
    efficiency_score,
    code_quality_score,
    problem_solving_score,
    time_score,
    machine_test_pipeline
)

def test_machine():
    # Specifications-requested test structure
    result = calculate_task_score(5, 10, 1.5, "print('hi')", 2)
    assert result["task_score"] > 0

def test_correctness_score():
    assert correctness_score(8, 10) == 0.8
    assert correctness_score(0, 5) == 0.0
    assert correctness_score(5, 0) == 0.0

def test_efficiency_score():
    assert efficiency_score(0.5) == 1.0
    assert efficiency_score(1.5) == 0.7
    assert efficiency_score(2.5) == 0.4

def test_code_quality_score():
    short_code = "print('hello')"
    long_code = "\n".join([f"line_{i}" for i in range(25)])
    very_long_code = "\n".join([f"line_{i}" for i in range(55)])
    
    assert code_quality_score(short_code) == 1.0
    assert code_quality_score(long_code) == 0.7
    assert code_quality_score(very_long_code) == 0.4

def test_problem_solving_score():
    assert problem_solving_score(1) == 1.0
    assert problem_solving_score(2) == 0.7
    assert problem_solving_score(4) == 0.4

def test_time_score():
    assert time_score(10, 30) == 1.0 # ratio 0.33 <= 0.5
    assert time_score(20, 30) == 0.7 # ratio 0.66 <= 1.0
    assert time_score(35, 30) == 0.4 # ratio 1.16 > 1.0

def test_machine_test_pipeline():
    data = {
        "candidate_id": "C5001",
        "task_id": "T101",
        "code_snapshot": "def add(a,b): return a+b",
        "execution_results": {
            "passed": 8,
            "total": 10,
            "runtime": 1.2
        },
        "attempts": 2,
        "time_taken": 25
    }
    
    res = machine_test_pipeline(data)
    assert res["final_score"] > 0
    assert "details" in res
