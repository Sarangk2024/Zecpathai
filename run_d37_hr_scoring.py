# run_d37_hr_scoring.py - Standalone HR interview scoring engine runner (Day 37).

import json
from interview_ai.hr_scoring_engine import hr_scoring_pipeline, score_hr_answer
from interview_ai.hr_weights import get_weights, normalize_interview_score

def main():
    print("\n==========================================================================================")
    print("ZECPATH HR INTERVIEW SCORING ENGINE RUNNER (DAY 37)")
    print("==========================================================================================\n")

    # Mock Answers
    answers = [
        {
            "question_id": "Q1",
            "relevance_score": 0.9,
            "communication_score": 85,
            "confidence_score": 80,
            "contradiction": False,
            "is_vague": False
        },
        {
            "question_id": "Q2",
            "relevance_score": 0.8,
            "communication_score": 75,
            "confidence_score": 60,
            "contradiction": True,
            "is_vague": False
        }
    ]

    # 1. Execute experienced pipeline
    print("--- [STEP 1] EXECUTING PIPELINE WITH EXPERIENCED WEIGHTS ---")
    result_exp = hr_scoring_pipeline(answers, "experienced")
    print(json.dumps(result_exp, indent=2))

    # 2. Execute fresher pipeline
    print("\n--- [STEP 2] EXECUTING PIPELINE WITH FRESHER WEIGHTS ---")
    result_fresh = hr_scoring_pipeline(answers, "fresher")
    print(json.dumps(result_fresh, indent=2))

    # 3. Normalization over length
    print("\n--- [STEP 3] NORMALIZING INTERVIEW TOTAL SCORES ---")
    total_score_exp = sum(d["final_score"] for d in result_exp["details"])
    norm_score = normalize_interview_score(total_score_exp, len(answers))
    print(f"Total Interview Raw Accumulation: {total_score_exp}")
    print(f"Normalized Average per Question:   {norm_score}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 37 HR Interview Scoring Engine Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
