# run_d49_integrity_detection.py

import json
from integrity_ai.detection_logic import detect_malpractice
from integrity_ai.risk_engine import calculate_integrity_score, risk_flagging, generate_warning, combined_risk

def main():
    print("\n==========================================================================================")
    print("ZECPATH MALPRACTICE & INTEGRITY DETECTION RUNNER (DAY 49)")
    print("==========================================================================================\n")

    # 1. Capture events and check flags
    print("--- [STEP 1] DETECTING MALPRACTICE FLAGS ---")
    events = {
        "tab_switch": 4,
        "focus_loss": 2,
        "voice_detect": 0,
        "gaze_off": 6
    }
    flags = detect_malpractice(events)
    print(f"Captured System Events: {events}")
    print(f"Malpractice Flags Generated: {flags}")

    # 2. Risk scoring engine
    print("\n--- [STEP 2] RUNNING RISK SCORING ENGINE ---")
    integrity_score = calculate_integrity_score(events)
    risk_lvl = risk_flagging(integrity_score)
    print(f"Calculated Integrity Score: {integrity_score}")
    print(f"System Risk Classification: {risk_lvl}")

    # 3. Warning prompt triggers
    print("\n--- [STEP 3] MOCKING USER INTERFACE WARNING ALERTS ---")
    warnings = generate_warning(events)
    for idx, w in enumerate(warnings, 1):
        print(f"Warning Alert #{idx}: [WARN] \"{w}\"")

    # 4. Behavioral integration combined score
    print("\n--- [STEP 4] COMBINING INTEGRITY & BEHAVIORAL RISKS ---")
    behavior_score = 80
    final_risk = combined_risk(behavior_score, integrity_score)
    print(f"Behavioral Score: {behavior_score} (40%) | Integrity Score: {integrity_score} (60%)")
    print(f"Combined Final Risk Index: {final_risk}")

    # 5. Output JSON payload sample
    print("\n--- [STEP 5] SAMPLE INTEGRITY PROFILE OUTPUT ---")
    candidate_profile = {
        "candidate_id": "C4001",
        "integrity_score": integrity_score,
        "risk_level": risk_lvl,
        "flags": flags,
        "warnings": warnings
    }
    print(json.dumps(candidate_profile, indent=2))

    # 6. Pattern Recognition Rules
    print("\n--- [STEP 6] INTEGRITY INTEGRATION RULES ---")
    rules = [
        "1. Repeated Tab Switch -> Possible cheating",
        "2. Continuous Voice Detection -> External help",
        "3. Gaze Off + Pause -> Looking at notes",
        "4. Focus Loss + Delay -> Distraction or multitasking"
    ]
    for r in rules:
        print(r)

    print("\n------------------------------------------------------------------------------------------")
    print("Day 49 Malpractice & Integrity Detection Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
