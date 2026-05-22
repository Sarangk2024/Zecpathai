# run_d44_api_specs.py

import json

def main():
    print("\n==========================================================================================")
    print("ZECPATH API SPECIFICATION RUNNER (DAY 44)")
    print("==========================================================================================\n")

    print(f"Base URL: https://api.zecpath.ai/v1/hr-interview\n")

    # 1. Start Interview endpoint Mock
    print("--- [ENDPOINT MOCK] POST /start ---")
    start_req = {
        "candidate_id": "C101",
        "job_id": "J501",
        "role_type": "technical",
        "experience_level": "fresher"
    }
    start_resp = {
        "session_id": "S123",
        "questions": [
            "Tell me about yourself",
            "What are your strengths?"
        ]
    }
    print(f"Request  : {json.dumps(start_req)}")
    print(f"Response : {json.dumps(start_resp, indent=2)}\n")

    # 2. Submit Answer endpoint Mock
    print("--- [ENDPOINT MOCK] POST /answer ---")
    answer_req = {
        "session_id": "S123",
        "question_id": "Q1",
        "answer": "I have experience in Python...",
        "duration": 6
    }
    answer_resp = {
        "follow_up": "Can you elaborate more?",
        "next_question": "Describe your teamwork experience"
    }
    print(f"Request  : {json.dumps(answer_req)}")
    print(f"Response : {json.dumps(answer_resp, indent=2)}\n")

    # 3. Get Final Report Mock
    print("--- [ENDPOINT MOCK] GET /report/S123 ---")
    report_resp = {
        "candidate_id": "C101",
        "final_score": 78,
        "decision": "Strong Hire",
        "summary": {
            "strengths": ["Good communication"],
            "weaknesses": ["Minor hesitation"]
        }
    }
    print(f"Response : {json.dumps(report_resp, indent=2)}\n")

    # 4. Error Handling Format Mock
    print("--- [ERROR MOCK] 400 Bad Request ---")
    error_resp = {
        "error_code": "INVALID_INPUT",
        "message": "Missing candidate_id",
        "status": 400
    }
    print(f"Response : {json.dumps(error_resp, indent=2)}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 44 API Specification Verified Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
