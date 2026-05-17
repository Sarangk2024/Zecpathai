# run_d34_followup_logic.py - Standalone dynamic follow-up logic runner (Day 34).

import json
from interview_ai.followup_pipeline import followup_pipeline
from interview_ai.state_tracker import InterviewState, avoid_repetition

def main():
    print("\n==========================================================================================")
    print("ZECPATH DYNAMIC FOLLOW-UP LOGIC RUNNER (DAY 34)")
    print("==========================================================================================\n")

    # 1. Pipeline Execution
    print("--- [STEP 1] EXECUTING FOLLOW-UP PIPELINE ---")
    test_cases = [
        {"q": "Tell me about your teamwork experience", "a": "I worked in a team", "conf": 0.6},
        {"q": "What is your notice period?", "a": "", "conf": 0.0},
        {"q": "Where do you see yourself in 5 years?", "a": "I am not sure, maybe lead", "conf": 0.5},
        {"q": "Explain a challenging technical problem you solved", "a": "I worked on projects using Python and Django to solve key business challenges.", "conf": 0.85}
    ]

    for tc in test_cases:
        res = followup_pipeline(tc["q"], tc["a"], tc["conf"])
        print(f"Base Question:  \"{tc['q']}\"")
        print(f"Answer:         \"{tc['a']}\" (Confidence: {tc['conf']})")
        print("Pipeline Output:")
        print(json.dumps(res, indent=2))
        print("-" * 50)

    # 2. State tracking
    print("\n--- [STEP 2] CONVERSATION STATE TRACKING & REPETITION PREVENTION ---")
    state = InterviewState()
    print("Adding interaction 'Tell me about your teamwork experience'...")
    state.add_interaction("Tell me about your teamwork experience", "I worked in a team")
    
    question_pool = [
        "Tell me about your teamwork experience",
        "What are your career goals?",
        "When can you join?"
    ]
    cleaned_pool = avoid_repetition(state, question_pool)
    print(f"Question Pool:    {question_pool}")
    print(f"Filtered Pool:    {cleaned_pool}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 34 Dynamic Follow-Up Logic Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
