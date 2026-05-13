# run_d26_scoring_engine.py - Standalone screening scoring engine runner (Day 26).

import json
from screening_ai.scoring_engine import (
    score_answer,
    screening_scoring_pipeline,
    explain_score
)

def main():
    print("\n==========================================================================================")
    print("ZECPATH SCREENING SCORING ENGINE RUNNER (DAY 26)")
    print("==========================================================================================\n")

    # 1. Example Answer to Score
    answer_q3 = {
        "question_id": "Q3",
        "original_text": "I have 3 years experience in Python",
        "intent": "experience",
        "skills": ["python"],
        "experience_years": 3,
        "availability": "Immediate",
        "off_topic": False,
        "is_vague": False
    }

    print("--- [STEP 1] PROCESSING AN ANSWER SCORING ---")
    scored_q3 = score_answer(answer_q3, "experience")
    print(f"Candidate Answer:  \"{answer_q3['original_text']}\"")
    print("Scored Output JSON:")
    print(json.dumps(scored_q3, indent=2))

    # 2. Explainable Scoring Output
    print("\n--- [STEP 2] EXPLAINABLE SCORING OUTPUT ---")
    explanation = explain_score(scored_q3)
    print(json.dumps(explanation, indent=2))

    # 3. Batch / Pipeline Execution
    print("\n--- [STEP 3] SCREENING SCORING PIPELINE RUN ---")
    answers = [
        {
            "question_id": "Q1",
            "original_text": "I am a senior python backend developer looking for a new role.",
            "intent": "introduction",
            "skills": ["python"],
            "experience_years": 5,
            "availability": "Unknown",
            "off_topic": False,
            "is_vague": False
        },
        {
            "question_id": "Q3",
            "original_text": "I have 3 years experience in Python",
            "intent": "experience",
            "skills": ["python"],
            "experience_years": 3,
            "availability": "Immediate",
            "off_topic": False,
            "is_vague": False
        },
        {
            "question_id": "Q6",
            "original_text": "I am looking for around 6 LPA and negotiable.",
            "intent": "salary",
            "skills": [],
            "experience_years": 0,
            "availability": "Unknown",
            "off_topic": False,
            "is_vague": False
        }
    ]
    intent_map = {
        "Q1": "introduction",
        "Q3": "experience",
        "Q6": "salary"
    }

    pipeline_result = screening_scoring_pipeline(answers, intent_map)
    print("Pipeline Output:")
    print(json.dumps(pipeline_result, indent=2))

    # 4. Final Screening Score Object format
    print("\n--- [STEP 4] FINAL SCREENING SCORE OBJECT ---")
    final_score_obj = {
        "candidate_id": "C123",
        "screening_score": pipeline_result["screening_score"],
        "decision": pipeline_result["decision"],
        "breakdown": [
            {"question_id": det["question_id"], "final_score": det["final_score"]}
            for det in pipeline_result["details"]
        ],
        "summary": {
            "avg_clarity": round(sum(d["scores"]["clarity"] for d in pipeline_result["details"]) / len(answers), 2),
            "avg_relevance": round(sum(d["scores"]["relevance"] for d in pipeline_result["details"]) / len(answers), 2),
            "avg_completeness": round(sum(d["scores"]["completeness"] for d in pipeline_result["details"]) / len(answers), 2),
            "avg_consistency": round(sum(d["scores"]["consistency"] for d in pipeline_result["details"]) / len(answers), 2),
        }
    }
    print(json.dumps(final_score_obj, indent=2))

    print("\n------------------------------------------------------------------------------------------")
    print("Day 26 Screening Scoring Engine Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
