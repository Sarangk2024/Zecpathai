# run_d39_summary_generator.py - Standalone interview summary generator runner (Day 39).

import json
from interview_ai.summary_generator import generate_interview_summary

def main():
    print("\n==========================================================================================")
    print("ZECPATH AI INTERVIEW SUMMARY GENERATOR RUNNER (DAY 39)")
    print("==========================================================================================\n")

    # Mock Data
    hr_scores = [
        {"question_id": "Q1", "final_score": 85},
        {"question_id": "Q2", "final_score": 45}
    ]
    communication = {
        "communication_score": 75.0,
        "breakdown": {}
    }
    behavior = {
        "confidence": {"confidence_score": 55.0},
        "contradiction": True,
        "behavioral_score": 60.0
    }
    answers = [
        "I worked in a team to build systems.",
        "Yes, but I don't know actually. I have experience in Java."
    ]

    print("--- [STEP 1] COMPILING INTERVIEW SUMMARY REPORT ---")
    summary = generate_interview_summary(
        candidate_id="C101",
        hr_scores=hr_scores,
        communication=communication,
        behavior=behavior,
        answers=answers
    )
    print("Report Summary Output JSON:")
    print(json.dumps(summary, indent=2))

    print("\n--- [STEP 2] NATURAL LANGUAGE GENERATOR OUTPUT ---")
    print(summary["natural_language_summary"])

    print("\n------------------------------------------------------------------------------------------")
    print("Day 39 Interview Summary Generator Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
