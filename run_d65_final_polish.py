# run_d65_final_polish.py

import json
from ai_core.final_production_system import production_pipeline, smooth_scores
from utils.final_error_handler import safe_run

def main():
    print("\n==========================================================================================")
    print("ZECPATH FINAL ENHANCEMENTS & PRODUCTION POLISH RUNNER (DAY 65)")
    print("==========================================================================================\n")

    # 1. Score Smoothing (Reducing outlier deviations)
    print("--- [STEP 1] EXECUTING SCORE SMOOTHING ---")
    raw_scores = {"ats": 95.0, "screening": 60.0, "hr": 80.0, "technical": 40.0, "machine_test": 75.0}
    print(f"Raw Scores:      {raw_scores}")
    smoothed = smooth_scores(raw_scores)
    print(f"Smoothed Scores: {smoothed}\n")

    # 2. Production Pipeline Evaluation
    print("--- [STEP 2] RUNNING PRODUCTION PIPELINE FOR CANDIDATES ---")
    
    # Strong Candidate C001
    scores_c001 = {"ats": 85, "screening": 80, "hr": 85, "technical": 88, "machine_test": 85}
    res_c001 = production_pipeline("C001", scores_c001)
    print("Candidate C001 (Strong):")
    print(json.dumps(res_c001, indent=2))
    
    # Average Candidate C002
    scores_c002 = {"ats": 65, "screening": 68, "hr": 70, "technical": 70, "machine_test": 65}
    res_c002 = production_pipeline("C002", scores_c002)
    print("\nCandidate C002 (Average):")
    print(json.dumps(res_c002, indent=2))

    # 3. Final Recruiter Summary Format
    print("\n--- [STEP 3] RECRUITER-FRIENDLY INSIGHTS SCHEMA ---")
    summary = {
        "candidate_id": "C001",
        "final_score": 84.8,
        "decision": "Selected",
        "summary": {
            "strengths": ["Strong technical skills", "Consistent performance across rounds"],
            "weaknesses": ["Minor communication gaps"],
            "risks": ["Low behavioral risk"]
        },
        "confidence": "High",
        "recommendation": "Proceed with offer letter"
    }
    print(json.dumps(summary, indent=2))

    # 4. Error Handling Checks
    print("\n--- [STEP 4] RUNNING FAIL-SAFE ERROR EXECUTION ---")
    def bad_runtime():
        raise KeyError("Score map key error: 'sandbox'")
    err_res = safe_run(bad_runtime, fallback="Scoring failed")
    print(json.dumps(err_res, indent=2))

    print("\n------------------------------------------------------------------------------------------")
    print("Day 65 System Polish Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
