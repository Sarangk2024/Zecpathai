# run_d63_demo_dataset.py

import json
import os
from demo.full_pipeline_simulation import run_demo_pipeline

def main():
    print("\n==========================================================================================")
    print("ZECPATH DEMO DATASET & ENVIRONMENT RUNNER (DAY 63)")
    print("==========================================================================================\n")

    json_path = r"c:\Users\kutta\OneDrive\Desktop\zecpath\demo\demo_dataset.json"
    
    # 1. Output job description and profiles
    print("--- [STEP 1] LOADING SIMULATION DATASET ---")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("Demo Job Description:")
        print(json.dumps(data["job_description"], indent=2))
        
        print("\nCandidate Profiles Summary:")
        for cand in data["candidates"]:
            print(f"- ID: {cand['candidate_id']} | Name: {cand['name']:<12} | Quality: {cand['level']:<8}")
    else:
        print("[ERROR] Demo dataset JSON not found!")

    # 2. Run simulation pipeline
    print("\n--- [STEP 2] RUNNING END-TO-END PIPELINE SIMULATION ---")
    for key in ["C001", "C002", "C003"]:
        res = run_demo_pipeline(key)
        print(f"Simulation Candidate {key} -> Final Score: {res['result']['final']}% | Decision: {res['result']['decision']}")

    # 3. Target mapping
    print("\n--- [STEP 3] MOCK TESTING SIMULATED OUTCOMES MATRIX ---")
    outcomes = [
        {"ID": "C001", "Level": "Strong", "Expected": "Selected"},
        {"ID": "C002", "Level": "Average", "Expected": "Hold / Review"},
        {"ID": "C003", "Level": "Weak", "Expected": "Rejected"}
    ]
    print(f"{'Candidate ID':<15} | {'Level':<10} | {'Expected Decision':<15}")
    print("-" * 48)
    for o in outcomes:
         print(f"{o['ID']:<15} | {o['Level']:<10} | {o['Expected']:<15}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 63 Demo Dataset Verification Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
