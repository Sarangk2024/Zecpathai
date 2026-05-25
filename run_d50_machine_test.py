# run_d50_machine_test.py

import json
from machine_test.evaluation_logic import calculate_task_score, machine_test_pipeline

def main():
    print("\n==========================================================================================")
    print("ZECPATH MACHINE TEST AI EVALUATION RUNNER (DAY 50)")
    print("==========================================================================================\n")

    # 1. Standard task scoring
    print("--- [STEP 1] EXECUTING STANDALONE TASK EVALUATION ---")
    result = calculate_task_score(
        passed=8,
        total=10,
        runtime=1.2,
        code="def add(a, b):\n    # add values\n    return a + b",
        attempts=2
    )
    print(f"Task Score Breakdown:")
    print(json.dumps(result, indent=2))

    # 2. Pipeline execution
    print("\n--- [STEP 2] RUNNING END-TO-END MACHINE TEST PIPELINE ---")
    candidate_data = {
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
    
    pipeline_res = machine_test_pipeline(candidate_data)
    print("Pipeline Output:")
    print(json.dumps(pipeline_res, indent=2))

    # 3. Sample output representation
    print("\n--- [STEP 3] SAMPLE EVALUATION REPORT OUTPUT ---")
    sample_output = {
        "candidate_id": "C5001",
        "task_score": pipeline_res["details"]["task_score"],
        "time_score": 70.0, # mocked for illustration matching example
        "final_score": 76.8,
        "decision": "Good Performance"
    }
    print(json.dumps(sample_output, indent=2))

    # 4. Scoring Model Formula Summary
    print("\n--- [STEP 4] SCORING FORMULA SPECIFICATIONS ---")
    formula = """
    Task Score =
      (Correctness x 0.4) +
      (Efficiency x 0.2) +
      (Code Quality x 0.2) +
      (Problem Solving x 0.2)
      
    Final Score =
      (Task Score x 0.8) +
      (Time Score x 0.2)
    """
    print(formula)

    # 5. Evaluation Metrics Table
    print("--- [STEP 5] EVALUATION METRICS DEFINITION ---")
    metrics = [
        {"metric": "Correctness", "desc": "Test case success percentage"},
        {"metric": "Efficiency", "desc": "Execution runtime performance"},
        {"metric": "Code Quality", "desc": "Readability & lines count structure"},
        {"metric": "Problem Solving", "desc": "Submission attempts & approach"},
        {"metric": "Time Score", "desc": "Task completion speed"}
    ]
    for m in metrics:
        print(f"Metric: {m['metric']:<16} | Description: {m['desc']}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 50 Machine Test AI Design Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
