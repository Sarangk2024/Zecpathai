# run_d57_stabilization.py

import json
from ai_core.stable_system import stable_pipeline
from utils.error_handler import safe_execute
from api.stable_api import api_response
from utils.edge_cases import handle_edge_cases
from utils.conversation_logic import next_step

def main():
    print("\n==========================================================================================")
    print("ZECPATH SYSTEM DEBUGGING & STABILIZATION RUNNER (DAY 57)")
    print("==========================================================================================\n")

    # 1. Out-of-bound scores cleaning pipeline
    print("--- [STEP 1] EXECUTING OUT-OF-BOUND SCORE CLEANUP ---")
    raw_scores = {"ats": 120, "hr": -10, "technical": "invalid_score", "screening": 85}
    print(f"Raw Input Scores: {raw_scores}")
    
    stable_res = stable_pipeline("C9001", raw_scores)
    print("Stable Pipeline Output:")
    print(json.dumps(stable_res, indent=2))

    # 2. Try-catch safe execution wrapper
    print("\n--- [STEP 2] TRY-CATCH SAFE EXECUTION WRAPPER ---")
    def bad_logic():
        raise ValueError("Division by zero in calculation engine")
        
    result_fault = safe_execute(bad_logic, default=0.0)
    print("Handled Exception Output:")
    print(json.dumps(result_fault, indent=2))

    # 3. Standardized API Response format
    print("\n--- [STEP 3] STANDARDIZED API RESPONSE FORMATS ---")
    success_resp = api_response(success=True, data={"candidate_id": "C9001", "score": 85.0})
    error_resp = api_response(success=False, error="Candidate profile not found in database")
    print(f"Success Response:\n{json.dumps(success_resp, indent=2)}")
    print(f"Error Response:\n{json.dumps(error_resp, indent=2)}")

    # 4. Input validation checking
    print("\n--- [STEP 4] INGESTION EDGE-CASE VERIFICATION ---")
    edge_cases = [
        "",
        "hello",
        "This is a valid detailed answer from candidate.",
        "a" * 1005
    ]
    for case in edge_cases:
        lbl = handle_edge_cases(case)
        print(f"Input text length: {len(case):>4} -> Classification: {lbl}")

    # 5. Conversation flow state transitions
    print("\n--- [STEP 5] CONVERSATIONAL DIALOG RETRY LIMIT TRANSITIONS ---")
    trans_states = [
        {"quality": "empty", "retry": 0},
        {"quality": "too_short", "retry": 1},
        {"quality": "empty", "retry": 3},
        {"quality": "valid", "retry": 0}
    ]
    for t in trans_states:
        action = next_step(t["quality"], t["retry"])
        print(f"Quality: {t['quality']:<10} | Retries: {t['retry']} -> Decision: {action}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 57 System Debugging & Stabilization Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
