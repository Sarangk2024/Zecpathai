# run_d33_interview_engine.py - Standalone HR interview engine design runner (Day 33).

import json
from interview_ai.question_generator import generate_questions

def main():
    print("\n==========================================================================================")
    print("ZECPATH HR INTERVIEW AI QUESTION GENERATION RUNNER (DAY 33)")
    print("==========================================================================================\n")

    # 1. Generate for Experienced Tech candidate
    print("--- [STEP 1] GENERATING QUESTIONS FOR EXPERIENCED TECHNICAL ROLE ---")
    questions_exp_tech = generate_questions("technical", "experienced")
    output_exp_tech = {
        "candidate_id": "C101",
        "role_type": "technical",
        "experience_level": "experienced",
        "questions": questions_exp_tech
    }
    print(json.dumps(output_exp_tech, indent=2))

    # 2. Generate for Fresher Non-Tech candidate
    print("\n--- [STEP 2] GENERATING QUESTIONS FOR FRESHER NON-TECHNICAL ROLE ---")
    questions_fresh_nontech = generate_questions("non_technical", "fresher")
    output_fresh_nontech = {
        "candidate_id": "C102",
        "role_type": "non_technical",
        "experience_level": "fresher",
        "questions": questions_fresh_nontech
    }
    print(json.dumps(output_fresh_nontech, indent=2))

    print("\n------------------------------------------------------------------------------------------")
    print("Day 33 HR Interview Engine Design Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
