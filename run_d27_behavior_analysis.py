# run_d27_behavior_analysis.py - Standalone confidence & sentiment analysis runner (Day 27).

import json
from screening_ai.behavior_report import generate_behavior_report

def main():
    print("\n==========================================================================================")
    print("ZECPATH CONFIDENCE & SENTIMENT SIGNAL ANALYSIS RUNNER (DAY 27)")
    print("==========================================================================================\n")

    # 1. Strong Example
    text_strong = "I am confident in my Python skills and have strong experience"
    duration_strong = 5
    print("--- [STEP 1] PROCESSING STRONG COMMUNICATION STATEMENT ---")
    print(f"Spoken Answer:  \"{text_strong}\" (Duration: {duration_strong}s)")
    report_strong = generate_behavior_report(text_strong, duration_strong)
    print("Behavioral Indicators Report (Output):")
    print(json.dumps(report_strong, indent=2))

    # 2. Hesitant / Uncertain Example
    text_weak = "Um, uh, maybe 3 years of work, but I'm not sure. Hmm."
    duration_weak = 10
    print("\n--- [STEP 2] PROCESSING HESITANT/WEAK STATEMENT ---")
    print(f"Spoken Answer:  \"{text_weak}\" (Duration: {duration_weak}s)")
    report_weak = generate_behavior_report(text_weak, duration_weak)
    print("Behavioral Indicators Report (Output):")
    print(json.dumps(report_weak, indent=2))

    print("\n------------------------------------------------------------------------------------------")
    print("Day 27 Confidence & Sentiment Signal Analysis Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
