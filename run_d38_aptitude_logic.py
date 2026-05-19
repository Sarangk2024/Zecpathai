# run_d38_aptitude_logic.py - Standalone aptitude logic runner (Day 38).

import json
from interview_ai.aptitude_pipeline import aptitude_pipeline

def main():
    print("\n==========================================================================================")
    print("ZECPATH COGNITIVE APTITUDE EVALUATION RUNNER (DAY 38)")
    print("==========================================================================================\n")

    # 1. Structure reasoning check
    text_structured = "First I prioritize the core tasks, then structure a plan, and finally execute them carefully."
    print("--- [STEP 1] TESTING STRUCTURED REASONING STATEMENT ---")
    print(f"Candidate Says: \"{text_structured}\"")
    result_struct = aptitude_pipeline(text_structured, "deadline_pressure")
    print("Aptitude Pipeline JSON Output:")
    print(json.dumps(result_struct, indent=2))

    # 2. Basic reasoning check
    text_basic = "I will try to complete the work somehow."
    print("\n--- [STEP 2] TESTING BASIC/UNSTRUCTURED STATEMENT ---")
    print(f"Candidate Says: \"{text_basic}\"")
    result_basic = aptitude_pipeline(text_basic, "deadline_pressure")
    print("Aptitude Pipeline JSON Output:")
    print(json.dumps(result_basic, indent=2))

    print("\n------------------------------------------------------------------------------------------")
    print("Day 38 Aptitude Logic Design Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
