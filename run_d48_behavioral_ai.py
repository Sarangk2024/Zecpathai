# run_d48_behavioral_ai.py

import json
from behavior_ai.signal_mapping import calculate_behavior_score, detect_behavior_risk

def main():
    print("\n==========================================================================================")
    print("ZECPATH BEHAVIORAL AI SIGNAL PROCESSING RUNNER (DAY 48)")
    print("==========================================================================================\n")

    # 1. Signal mapping sample execution
    print("--- [STEP 1] EXECUTING SIGNAL-TO-SCORE MAPPING ---")
    signals = {
        "eye_focus": 0.8,
        "head_stability": 0.7,
        "engagement": 0.9,
        "distraction": 0.2
    }
    score = calculate_behavior_score(signals)
    risk = detect_behavior_risk(score)
    print(f"Input Signals: {signals}")
    print(f"Calculated Behavioral Score: {score}")
    print(f"Behavioral Risk Status     : {risk}")

    # 2. Risk Detection Logic
    print("\n--- [STEP 2] BEHAVIORAL RISK DETECTION MAPPINGS ---")
    test_scores = [88.5, 68.0, 45.0]
    for s in test_scores:
        print(f"Behavior Score: {s:>5} -> Risk Classification: {detect_behavior_risk(s)}")

    # 3. Sample Behavioral Output
    print("\n--- [STEP 3] SAMPLE BEHAVIORAL REPORT OBJECT ---")
    report = {
        "behavior_score": score,
        "signals": signals,
        "insights": {
            "focus_level": "High" if signals["eye_focus"] >= 0.8 else "Medium",
            "engagement": "Strong" if signals["engagement"] >= 0.8 else "Moderate",
            "risk": f"{risk} distraction"
        }
    }
    print(json.dumps(report, indent=2))

    # 4. Behavioral Scoring Levels
    print("\n--- [STEP 4] BEHAVIORAL SCORING LEVELS MATRIX ---")
    levels = [
        {"range": "85-100", "status": "Highly Focused"},
        {"range": "70-84", "status": "Good Engagement"},
        {"range": "50-69", "status": "Moderate"},
        {"range": "< 50", "status": "Distracted / Low Focus"}
    ]
    for l in levels:
        print(f"Score Range: {l['range']:<10} -> Behavior Status: {l['status']}")

    # 5. Ethical Guidelines
    print("\n--- [STEP 5] ETHICAL CONSIDERATIONS ---")
    print("- No facial recognition storage")
    print("- No identity tracking")
    print("- Only behavioral metadata stored")
    print("- Candidate consent required")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 48 Behavioral AI Signal Processing Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
