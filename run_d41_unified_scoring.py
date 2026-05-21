# run_d41_unified_scoring.py - Standalone unified scoring engine runner (Day 41).

import json
from ai_core.unified_scoring_engine import calculate_unified_score, get_weights, unified_scoring_pipeline

def main():
    print("\n==========================================================================================")
    print("ZECPATH UNIFIED SCORING ENGINE RUNNER (DAY 41)")
    print("==========================================================================================\n")

    # 1. Direct score calculation demo
    print("--- [STEP 1] EXECUTING SCORE CALCULATION ---")
    score = calculate_unified_score(80, 70, 85, {
        "ats": 0.3,
        "screening": 0.3,
        "hr": 0.4
    })
    print(f"ATS: 80 | Screening: 70 | HR: 85 | Weights: 30%/30%/40%")
    print(f"Final Integrated Weighted Score: {score}")

    # 2. Pipeline examples: Strong, Average, Weak
    print("\n--- [STEP 2] RUNNING BATCH CANDIDATE PIPELINES ---")
    
    # Strong Experienced Candidate
    report_strong = unified_scoring_pipeline("C101", 88, 80, 87, "experienced")
    print("\nCandidate 1 (Strong Experienced):")
    print(json.dumps(report_strong, indent=2))
    
    # Average Fresher Candidate
    report_avg = unified_scoring_pipeline("C102", 60, 68, 60, "fresher")
    print("\nCandidate 2 (Average Fresher):")
    print(json.dumps(report_avg, indent=2))
    
    # Weak Candidate
    report_weak = unified_scoring_pipeline("C103", 40, 50, 45, "non_technical")
    print("\nCandidate 3 (Weak Non-Technical):")
    print(json.dumps(report_weak, indent=2))

    print("\n------------------------------------------------------------------------------------------")
    print("Day 41 Unified Scoring Engine Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
