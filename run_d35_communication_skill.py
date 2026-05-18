# run_d35_communication_skill.py - Standalone communication skill evaluation runner (Day 35).

import json
from interview_ai.communication_engine import calculate_communication_score
from interview_ai.normalization import normalize_score

def main():
    print("\n==========================================================================================")
    print("ZECPATH COMMUNICATION SKILL EVALUATION RUNNER (DAY 35)")
    print("==========================================================================================\n")

    # 1. Sample strong communication
    text_strong = "I have experience in Python because I worked on backend systems. For example, I built several APIs."
    print("--- [STEP 1] EVALUATING EXCELLENT COMMUNICATION SAMPLE ---")
    print(f"Candidate Says: \"{text_strong}\"")
    result_strong = calculate_communication_score(text_strong)
    print("Communication Score JSON Output:")
    print(json.dumps(result_strong, indent=2))

    # 2. Sample average communication (some fillers)
    text_avg = "Actually I know python basically. I worked on some projects, you know, for some client."
    print("\n--- [STEP 2] EVALUATING GOOD/AVERAGE COMMUNICATION ---")
    print(f"Candidate Says: \"{text_avg}\"")
    result_avg = calculate_communication_score(text_avg)
    print("Communication Score JSON Output:")
    print(json.dumps(result_avg, indent=2))

    # 3. Sample weak communication (very short and lots of fillers)
    text_weak = "um uh like i worked"
    print("\n--- [STEP 3] EVALUATING WEAK COMMUNICATION ---")
    print(f"Candidate Says: \"{text_weak}\"")
    result_weak = calculate_communication_score(text_weak)
    print("Communication Score JSON Output:")
    print(json.dumps(result_weak, indent=2))

    # 4. Bias Normalization
    print("\n--- [STEP 4] RUNNING BIAS NORMALIZATION DEMO ---")
    raw_score = result_avg["communication_score"]
    normalized = normalize_score(raw_score, min_val=20, max_val=90)
    print(f"Raw Communication Score:       {raw_score}")
    print(f"Normalized (Min: 20, Max: 90): {normalized}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 35 Communication Skill Evaluation Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
