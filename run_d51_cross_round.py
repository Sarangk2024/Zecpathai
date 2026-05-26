# run_d51_cross_round.py

import json
from ai_core.cross_round_engine import calculate_final_score, aggregation_pipeline

def main():
    print("\n==========================================================================================")
    print("ZECPATH CROSS-ROUND AGGREGATION ENGINE RUNNER (DAY 51)")
    print("==========================================================================================\n")

    # 1. Direct calculation check
    print("--- [STEP 1] EXECUTING BASIC CALCULATION ---")
    scores_simple = {
        "ats": 70, "screening": 70, "hr": 70, "technical": 70, "machine_test": 70
    }
    weights_simple = {
        "ats": 0.2, "screening": 0.2, "hr": 0.2, "technical": 0.2, "machine_test": 0.2
    }
    score = calculate_final_score(scores_simple, weights_simple)
    print(f"Scores: {scores_simple}")
    print(f"Weights: {weights_simple} -> Final: {score}\n")

    # 2. Pipeline examples: Strong, Average, Weak
    print("--- [STEP 2] PIPELINE EXECUTION FOR VARIOUS ROLES ---")
    
    # Technical Candidate (Strong)
    scores_strong = {"ats": 75, "screening": 70, "hr": 80, "technical": 85, "machine_test": 78}
    res_strong = aggregation_pipeline("C9001", scores_strong, "technical")
    print("\nStrong Technical Candidate:")
    print(json.dumps(res_strong, indent=2))
    
    # Fresher Candidate (Average)
    scores_avg = {"ats": 60, "screening": 68, "hr": 65, "technical": 62, "machine_test": 55}
    res_avg = aggregation_pipeline("C9002", scores_avg, "fresher")
    print("\nAverage Fresher Candidate:")
    print(json.dumps(res_avg, indent=2))
    
    # Non-Technical Candidate (Weak)
    scores_weak = {"ats": 45, "screening": 50, "hr": 48, "technical": 40, "machine_test": 45}
    res_weak = aggregation_pipeline("C9003", scores_weak, "non_technical")
    print("\nWeak Non-Technical Candidate:")
    print(json.dumps(res_weak, indent=2))

    # 3. Explainable Score Breakdown Example
    print("\n--- [STEP 3] EXPLAINABLE SCORE BREAKDOWN EXAMPLE ---")
    breakdown = {
        "explanation": {
            "ats": "Good resume-job match",
            "screening": "Clear responses with minor gaps",
            "hr": "Strong communication and confidence",
            "technical": "High technical depth",
            "machine_test": "Good practical coding performance"
        }
    }
    print(json.dumps(breakdown, indent=2))

    print("\n------------------------------------------------------------------------------------------")
    print("Day 51 Cross-Round Aggregation Engine Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
