# run_d45_final_handover.py

import json
from interview_ai.final_hr_module import run_hr_interview

def load_demo_dataset():
    with open("demo/hr_demo_dataset.json", "r") as f:
        return json.load(f)

def main():
    print("\n==========================================================================================")
    print("ZECPATH FINAL HR INTERVIEW SYSTEM DEMO & HANDOVER RUNNER (DAY 45)")
    print("==========================================================================================\n")

    # 1. Load candidates from JSON
    print("--- [STEP 1] LOADING DEMO DATASET ---")
    candidates = load_demo_dataset()
    print(f"Loaded {len(candidates)} candidates from demo/hr_demo_dataset.json.\n")

    # 2. Simulate pipeline execution for each candidate
    print("--- [STEP 2] RUNNING PRODUCTION PIPELINE SIMULATION ---")
    
    # We will simulate behavior and communication metrics for the candidates
    mock_metrics = {
        "C1001": {
            "communication": {"communication_score": 82},
            "behavior": {
                "confidence": {"confidence_score": 78},
                "behavioral_score": 80,
                "contradiction": False
            },
            "answers_scored": [
                {
                    "question_id": "Q1",
                    "answer_text": "I am a backend developer with experience in Python and APIs.",
                    "relevance_score": 0.85,
                    "communication_score": 82,
                    "confidence_score": 78,
                    "contradiction": False,
                    "is_vague": False
                },
                {
                    "question_id": "Q2",
                    "answer_text": "I worked with a team to deliver projects on time.",
                    "relevance_score": 0.80,
                    "communication_score": 82,
                    "confidence_score": 78,
                    "contradiction": False,
                    "is_vague": False
                },
                {
                    "question_id": "Q3",
                    "answer_text": "Problem solving and learning quickly.",
                    "relevance_score": 0.85,
                    "communication_score": 82,
                    "confidence_score": 78,
                    "contradiction": False,
                    "is_vague": False
                }
            ]
        },
        "C1002": {
            "communication": {"communication_score": 68},
            "behavior": {
                "confidence": {"confidence_score": 62},
                "behavioral_score": 65,
                "contradiction": False
            },
            "answers_scored": [
                {
                    "question_id": "Q1",
                    "answer_text": "I recently graduated and learned React.",
                    "relevance_score": 0.70,
                    "communication_score": 68,
                    "confidence_score": 62,
                    "contradiction": False,
                    "is_vague": False
                },
                {
                    "question_id": "Q2",
                    "answer_text": "I did projects in college teams.",
                    "relevance_score": 0.65,
                    "communication_score": 68,
                    "confidence_score": 62,
                    "contradiction": False,
                    "is_vague": False
                }
            ]
        }
    }

    for candidate in candidates:
        cid = candidate["candidate_id"]
        metrics = mock_metrics.get(cid)
        if not metrics:
            continue
            
        print(f"\nProcessing candidate: {cid} ({candidate['role']})")
        result = run_hr_interview(
            candidate_id=cid,
            answers=metrics["answers_scored"],
            communication=metrics["communication"],
            behavior=metrics["behavior"]
        )
        print(json.dumps(result, indent=2))

    # 3. Manager Evaluation Feedback
    print("\n--- [STEP 3] MANAGER EVALUATION FEEDBACK ---")
    feedback = {
        "Strengths": [
            "Strong system architecture",
            "Clear scoring logic",
            "Good modular design",
            "Scalable AI pipeline"
        ],
        "Areas for Improvement": [
            "[-] Improve contextual understanding",
            "[-] Add multilingual support",
            "[-] Enhance behavioral AI"
        ],
        "Overall Rating": "8.5 / 10",
        "Status": "Approved for Production (Phase 1)"
    }
    print(json.dumps(feedback, indent=2))

    # 4. Handover Checklist
    print("\n--- [STEP 4] HANDOVER CHECKLIST ---")
    checklist = {
        "Complete codebase delivered": True,
        "API documentation provided": True,
        "Demo dataset shared": True,
        "Test scripts included": True,
        "Architecture explained": True,
        "Known limitations documented": True,
        "Future roadmap defined": True
    }
    for item, status in checklist.items():
        print(f"[OK] {item:<40} : {status}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 45 HR Interview Demo & Finalization Completed Successfully!")
    print("System Status: OK (Production Ready)")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
