# run_d36_confidence_stress.py - Standalone confidence & stress indicators runner (Day 36).

import json
from interview_ai.behavior_analyzer import analyze_behavior

def main():
    print("\n==========================================================================================")
    print("ZECPATH CONFIDENCE & STRESS INDICATORS RUNNER (DAY 36)")
    print("==========================================================================================\n")

    # 1. Confident behavior sample
    text_confident = "I am confident in my Python skills and achieved strong success."
    duration_conf = 5
    print("--- [STEP 1] EVALUATING CONFIDENT BEHAVIOR STATEMENT ---")
    print(f"Spoken Answer:  \"{text_confident}\" (Duration: {duration_conf}s)")
    report_conf = analyze_behavior(text_confident, duration_conf)
    print("Behavioral Score Report:")
    print(json.dumps(report_conf, indent=2))

    # 2. Stressed/Uncertain behavior sample
    text_stressed = "I think I am confident but maybe I need improvement, sorry."
    duration_stressed = 6
    print("\n--- [STEP 2] EVALUATING STRESSED & CONTRADICTORY STATEMENT ---")
    print(f"Spoken Answer:  \"{text_stressed}\" (Duration: {duration_stressed}s)")
    report_stressed = analyze_behavior(text_stressed, duration_stressed)
    print("Behavioral Score Report:")
    print(json.dumps(report_stressed, indent=2))

    print("\n------------------------------------------------------------------------------------------")
    print("Day 36 Confidence & Stress Indicators Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
