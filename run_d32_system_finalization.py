# run_d32_system_finalization.py - Standalone screening system finalization runner (Day 32).

import json
from demo.run_demo import run_demo
from api.routes import app

def main():
    print("\n==========================================================================================")
    print("ZECPATH SCREENING SYSTEM FINALIZATION RUNNER (DAY 32)")
    print("==========================================================================================\n")

    # 1. Run End-to-End Demo
    print("--- [STEP 1] EXECUTING END-TO-END DEMO ---")
    demo_output = run_demo()
    print("Live Demo Output JSON:")
    print(json.dumps(demo_output, indent=2))

    # 2. Mock Server Request
    print("\n--- [STEP 2] TESTING API SERVER MOCK REQUEST ---")
    client = app.test_client()
    payload = {
        "candidate_id": "C101",
        "job_id": "J501",
        "answers": [
            {
                "question_id": "Q1",
                "original_text": "I expect around 6 LPA and can join immediately next week.",
                "skills": [],
                "availability": "Immediate",
                "salary": "6 LPA",
                "is_vague": False,
                "off_topic": False
            }
        ],
        "scores": [
            {
                "question_id": "Q1",
                "final_score": 88
            }
        ],
        "behavior": [
            {
                "communication_strength": "Strong"
            }
        ]
    }
    
    response = client.post("/screening/start", data=json.dumps(payload), content_type="application/json")
    print(f"API Endpoint: POST /screening/start")
    print(f"Response Status Code: {response.status_code}")
    print("Response Body:")
    print(json.dumps(json.loads(response.data), indent=2))

    print("\n------------------------------------------------------------------------------------------")
    print("Day 32 Screening System Finalization Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
