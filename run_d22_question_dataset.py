# run_d22_question_dataset.py - Standalone screening questions dataset verification runner (Day 22).

import json
import os
from screening_ai.question_templates import (
    generate_skill_question,
    generate_experience_question,
    generate_location_question,
    load_questions
)

def main():
    print("\n==========================================================================================")
    print("ZECPATH HR SCREENING QUESTION DATASET RUNNER (DAY 22)")
    print("==========================================================================================")
    
    # 1. Load basic dataset
    dataset_path = "data/hr_screening_dataset.json"
    questions = load_questions(dataset_path)
    print(f"\n--- [STEP 1] LOADED BASIC SCREENING QUESTIONS ({len(questions)} items) ---")
    for q in questions[:3]:
        print(f"  - [{q['question_id']}] ({q['category']}): \"{q['question']}\" (Importance: {q['importance']})")
        
    # 2. Print category mapping
    mapping_path = "data/question_category_mapping.json"
    mappings = load_questions(mapping_path)
    print("\n--- [STEP 2] QUESTION CATEGORY AND WEIGHT MAPPING ---")
    print(json.dumps(mappings, indent=2))
    
    # 3. Load Multilingual Conversation-Ready Objects
    multilingual_path = "screening_ai/question_objects.json"
    ml_questions = load_questions(multilingual_path)
    print("\n--- [STEP 3] MULTILINGUAL CONVERSATION-READY QUESTION OBJECTS ---")
    print(json.dumps(ml_questions, indent=2))
    
    # 4. Reusable templates demo
    print("\n--- [STEP 4] REUSABLE QUESTION TEMPLATES DEMO ---")
    print("Skill Template (Backend Developer): ", generate_skill_question("Backend Developer"))
    print("Experience Template (CNC Machinist):", generate_experience_question("CNC Machinist"))
    print("Location Template:                 ", generate_location_question())
    
    # 5. Example screening flow
    flow_schema = {
        "flow": [
            "Q1 - Introduction",
            "Q2 - Education",
            "Q3 - Experience",
            "Q4 - Skills",
            "Q5 - Location",
            "Q7 - Notice Period",
            "Q6 - Salary (optional)"
        ]
    }
    print("\n--- [STEP 5] STANDARD CONVERSATION FLOW ROUTE ---")
    print(json.dumps(flow_schema, indent=2))
    
    print("\n------------------------------------------------------------------------------------------")
    print("Day 22 HR Screening Dataset Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
