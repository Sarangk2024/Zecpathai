# run_d25_answer_engine.py - Standalone answer intent and understanding engine runner (Day 25).

import json
from screening_ai.answer_engine import process_answer, process_answers_batch

def main():
    print("\n==========================================================================================")
    print("ZECPATH ANSWER INTENT & UNDERSTANDING ENGINE RUNNER (DAY 25)")
    print("==========================================================================================")
    
    # 1. Processing a Single Experience Answer (With Skills & Experience)
    print("\n--- [STEP 1] PROCESSING AN EXPERIENCE RESPONSE ---")
    exp_answer = "I have 3 years experience in Python and Django"
    result_exp = process_answer("Q3", exp_answer)
    print("Candidate Answer: ", exp_answer)
    print("Structured Output JSON:")
    print(json.dumps(result_exp, indent=2))
    
    # 2. Processing Logistical Responses (Salary + Notice Period)
    print("\n--- [STEP 2] PROCESSING LOGISTICS RESPONSE (SALARY + AVAILABILITY) ---")
    salary_answer = "I expect around 6 LPA and can join immediately next week."
    result_salary = process_answer("Q6", salary_answer)
    print("Candidate Answer: ", salary_answer)
    print("Structured Output JSON:")
    print(json.dumps(result_salary, indent=2))
    
    # 3. Quality Flags: Vague Response Check
    print("\n--- [STEP 3] DETECTING VAGUE CANDIDATE ANSWERS ---")
    vague_answer = "Maybe 3 years of work, but I'm not sure."
    result_vague = process_answer("Q3", vague_answer)
    print("Candidate Answer: ", vague_answer)
    print(f"Is Vague Flag:     {result_vague['is_vague']}")
    
    # 4. Quality Flags: Off-topic Response Check
    print("\n--- [STEP 4] DETECTING OFF-TOPIC ANSWERS ---")
    off_topic_answer = "I love watching football on Sundays with my friends."
    result_off_topic = process_answer("Q1", off_topic_answer)
    print("Candidate Answer: ", off_topic_answer)
    print(f"Is Off-topic Flag: {result_off_topic['off_topic']}")
    
    # 5. Batch Process answers
    print("\n--- [STEP 5] BATCH EVALUATION PIPELINE RUN ---")
    answers_batch = [
        {"question_id": "Q1", "text": "Let me introduce myself, I am a Python engineer"},
        {"question_id": "Q3", "text": "I worked in the tooling shop for 5 years"},
        {"question_id": "Q6", "text": "My expectation is 80k monthly"},
        {"question_id": "Q7", "text": "   "} # empty answer
    ]
    batch_results = process_answers_batch(answers_batch)
    
    print("\nBatch Structured Summaries:")
    print(f"{'QID':<5} | {'Intent':<13} | {'Skills':<18} | {'Exp (Yrs)':<10} | {'Salary':<10} | {'Vague':<6} | {'Off-Topic':<8}")
    print("-" * 85)
    for r in batch_results:
        skills_str = ", ".join(r["skills"]) if r["skills"] else "None"
        print(f"{r['question_id']:<5} | {r['intent']:<13} | {skills_str:<18} | {r['experience_years']:<10} | {str(r['salary']):<10} | {str(r['is_vague']):<6} | {str(r['off_topic']):<8}")
        
    print("\n------------------------------------------------------------------------------------------")
    print("Day 25 Answer Intent & Understanding Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
