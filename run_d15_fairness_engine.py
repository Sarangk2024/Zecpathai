# run_fairness_engine.py - Standalone runner to check Day 15 (Fairness/Bias Engine)

import os
import json
import sys
from ats_engine.fairness_engine import normalize_scores, mask_sensitive_data, generate_fair_score
from utils.logger import logger

def main():
    logger.info("Initializing Day 15 Fairness/Bias Engine Check...")
    
    rankings_dir = "data/ats_rankings"
    output_dir = "data/ats_fairness"
    
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(rankings_dir) or not os.listdir(rankings_dir):
        print("Note: run_ranking_engine.py outputs not found. Running ranking engine first...")
        from run_ranking_engine import main as run_ranker
        run_ranker()
        
    rankings_path = os.path.join(rankings_dir, "ranked_candidates.json")
    with open(rankings_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        candidates = data.get("ranked_list", [])
        
    print("\n==========================================================================================")
    print("ZECPATH FAIRNESS, NORMALIZATION & BIAS REDUCTION RUNNER (DAY 15)")
    print("==========================================================================================")
    print(f"Rankings Input: {rankings_dir}")
    print(f"Output Folder:  {output_dir}\n")
    
    # Apply Day 15 Engines
    for c in candidates:
        generate_fair_score(c)
        
    candidates = normalize_scores(candidates)
    
    masked_candidates = []
    for c in candidates:
        c_copy = c.copy()
        c_profile = {
            "candidate_id": c.get("candidate_id"),
            "name": c.get("candidate_id").replace("_cleaned", "").replace("_", " ").title(),
            "gender": "Male" if "sarang" in c.get("candidate_id").lower() else "Not Specified",
            "location": "Kerala" if "sarang" in c.get("candidate_id").lower() else "India",
            "email": f"{c.get('candidate_id').lower()}@example.com",
            "phone": "91-9988776655"
        }
        masked_profile = mask_sensitive_data(c_profile)
        c_copy["masked_profile"] = masked_profile
        masked_candidates.append(c_copy)
        
    print(f"{'Candidate Resume Filename':<48} | {'Raw Score':<9} | {'Norm Score':<10} | {'Fair Score':<10} | {'Masked Profile Name'}")
    print("-" * 115)
    
    for c in masked_candidates:
        print(
            f"{c['candidate_id'] + '_cleaned.txt':<48} | "
            f"{c['final_score']:<9.2f} | {c['normalized_score']:<10.2f} | "
            f"{c['fair_score']:<10.2f} | {c['masked_profile'].get('name')}"
        )
        
    with open(os.path.join(output_dir, "fair_candidates.json"), "w", encoding="utf-8") as out_f:
        json.dump(masked_candidates, out_f, indent=2)
        
    print("\n------------------------------------------------------------------------------------------")
    print("Fairness, Normalization, and Bias Reduction Run Completed Successfully!")
    print(f"PII masked profile keys: name, email, location, phone, gender -> MASKED")
    print(f"Structured outputs saved to: {os.path.abspath(output_dir)}")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
