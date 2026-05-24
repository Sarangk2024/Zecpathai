# run_d47_technical_scoring.py

import json
from technical_ai.technical_scoring_engine import calculate_technical_score, technical_pipeline

def main():
    print("\n==========================================================================================")
    print("ZECPATH TECHNICAL SKILL SCORING RUNNER (DAY 47)")
    print("==========================================================================================\n")

    # 1. Example execution from spec
    print("--- [STEP 1] EXECUTING RAW ANSWER SCORING ---")
    text = "First I design architecture, then optimize for scalability because real-world systems need performance."
    result = calculate_technical_score(text, True)
    print(f"Candidate Answer: \"{text}\"")
    print(json.dumps(result, indent=2))

    # 2. Pipeline with Normalization
    print("\n--- [STEP 2] PIPELINE EXECUTION WITH DIFFICULTY NORMALIZATION ---")
    scenarios = [
        {"answer": "closures are functions with preserved state", "diff": "basic", "correct": True},
        {"answer": "First we check keys, then extract maps because database requires it", "diff": "intermediate", "correct": True},
        {"answer": "First I design architecture, then optimize for scalability because real-world systems need performance.", "diff": "advanced", "correct": True}
    ]
    for s in scenarios:
        pipe_res = technical_pipeline(s["answer"], s["diff"], s["correct"])
        print(f"\nDifficulty: {s['diff']:<12} | Correct: {s['correct']}")
        print(f"Final Normalized Score: {pipe_res['final_score']}")
        print(f"Base Score             : {pipe_res['details']['technical_score']}")

    # 3. Skill-Wise breakdown example
    print("\n--- [STEP 3] SKILL-WISE BREAKDOWN SAMPLE ---")
    skills_breakdown = {
        "skills": {
            "JavaScript": 82,
            "React": 75,
            "Node.js": 78
        },
        "overall_technical_score": 78.3
    }
    print(json.dumps(skills_breakdown, indent=2))

    # 4. Technical Evaluation Report Format
    print("\n--- [STEP 4] TECHNICAL EVALUATION REPORT FORMAT ---")
    report = {
        "candidate_id": "C3001",
        "technical_score": 81.5,
        "decision": "Strong Technical Fit",
        "breakdown": [
            {
                "question_id": "Q1",
                "score": 85,
                "depth": "deep",
                "explanation": "Strong conceptual clarity and real-world understanding"
            }
        ],
        "skills": {
            "Python": 80,
            "System Design": 75
        },
        "strengths": [
            "Strong problem-solving",
            "Good system thinking"
        ],
        "weaknesses": [
            "Limited optimization discussion"
        ]
    }
    print(json.dumps(report, indent=2))

    # 5. Explainability Notes
    print("\n--- [STEP 5] EXPLAINABLE OUTPUT DETAILS ---")
    explanation = {
        "question_id": "Q2",
        "explanation": {
            "accuracy": "Correct answer",
            "depth": "Explained with examples",
            "logic": "Step-by-step reasoning present",
            "real_world": "Linked to production use case"
        }
    }
    print(json.dumps(explanation, indent=2))

    print("\n------------------------------------------------------------------------------------------")
    print("Day 47 Technical Skill Scoring Model Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
