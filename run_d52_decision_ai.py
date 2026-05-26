# run_d52_decision_ai.py

import json
from ai_core.decision_engine import generate_decision, calculate_decision_confidence, recommendation_pipeline

def main():
    print("\n==========================================================================================")
    print("ZECPATH FINAL RECOMMENDATION AI RUNNER (DAY 52)")
    print("==========================================================================================\n")

    # 1. Base decision generation check
    print("--- [STEP 1] EXECUTING DECISION GENERATION ---")
    decision, score = generate_decision(85)
    print(f"Base Score: 85 -> Decision: {decision} | Score: {score}\n")

    # 2. Recommendation pipeline checks
    print("--- [STEP 2] RUNNING RECOMMENDATION PIPELINE FOR CANDIDATES ---")
    
    # Selected Candidate (High Score, Low Risk)
    scores_sel = {"ats": 82, "screening": 80, "hr": 84, "technical": 85, "machine_test": 82, "final_score": 82.5}
    res_sel = recommendation_pipeline("C10001", scores_sel, "Low Risk", "Low Risk")
    print("\nSelected Candidate (Low Risk):")
    print(json.dumps(res_sel, indent=2))
    
    # Hold Candidate (High Score, Moderate Integrity Risk -> Penalty -7)
    res_hold = recommendation_pipeline("C10002", scores_sel, "Low Risk", "Moderate Risk")
    print("\nHold Candidate (Moderate Integrity Risk -> -7 Penalty):")
    print(json.dumps(res_hold, indent=2))

    # Rejected Candidate (Low Score, High Risk -> Penalty -10 -15 = -25)
    scores_weak = {"ats": 60, "screening": 58, "hr": 62, "technical": 55, "machine_test": 50, "final_score": 57.0}
    res_rej = recommendation_pipeline("C10003", scores_weak, "High Risk", "High Risk")
    print("\nRejected Candidate (High Risk -> -25 Penalty):")
    print(json.dumps(res_rej, indent=2))

    # 3. Decision Flow output description
    print("\n--- [STEP 3] DECISION WORKFLOW PROGRESSION ---")
    flow = """
    Input Scores + Risk Factors
               ↓
    Adjust Score (Risk Penalty)
               ↓
    Apply Thresholds
               ↓
    Generate Decision
               ↓
    Calculate Confidence
               ↓
    Generate Explanation
               ↓
    Final Output Object
    """
    print(flow.replace("↓", "|"))

    print("------------------------------------------------------------------------------------------")
    print("Day 52 Recommendation AI Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
