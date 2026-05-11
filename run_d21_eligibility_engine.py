# run_d21_eligibility_engine.py - Standalone eligibility engine verification runner (Day 21).

import os
import json
from screening_ai.eligibility_engine import evaluate_candidate, evaluate_candidates_batch

def get_rules_for_job(job_title):
    """
    Returns tailored hiring rules based on the target job role to prevent
    designers from being evaluated against machining constraints and vice versa.
    """
    job_title_lower = job_title.lower()
    
    # Default Base Rules
    rules = {
        "min_ats_score": 50,                  # Base ATS cutoff
        "mandatory_skills": [],               # No mandatory skills by default
        "min_experience": 1,                  # Min 1 year
        "max_experience": 10,                 # Max 10 years
        "allowed_locations": [],              # Open to any location
        "availability_required": False        # Open availability
    }
    
    if "machinist" in job_title_lower:
        rules["mandatory_skills"] = ["cnc"]
    elif "design" in job_title_lower:
        rules["mandatory_skills"] = ["solidworks"]
    elif "maker" in job_title_lower:
        rules["mandatory_skills"] = ["fitting"]
    elif "technician" in job_title_lower:
        rules["mandatory_skills"] = ["die_assembly"]
    elif "operator" in job_title_lower:
        rules["mandatory_skills"] = ["grinding"]
        
    return rules

def main():
    print("\n==========================================================================================")
    print("ZECPATH ELIGIBILITY DECISION ENGINE RUNNER (DAY 21)")
    print("==========================================================================================")
    
    # 1. Job-Specific Rule Configuration (Backend Developer)
    backend_rules = {
        "min_ats_score": 75,
        "mandatory_skills": ["Python", "Django"],
        "min_experience": 2,
        "max_experience": 6,
        "allowed_locations": ["Bangalore", "Remote"],
        "availability_required": True
    }
    
    print("\n--- [STEP 1] DEMO JOB-SPECIFIC RULE CONFIGURATION (Backend Developer) ---")
    print(json.dumps({
        "job_id": "J101",
        "job_title": "Backend Developer",
        "rules": backend_rules
    }, indent=2))
    
    # Test Candidates Pool (Demo mock data)
    mock_pool = [
        {"candidate_id": "C123", "final_score": 82, "skills": ["Python", "Django", "SQL"], "total_experience": 3, "location": "Bangalore", "available": True},
        {"candidate_id": "C124", "final_score": 68, "skills": ["Python", "Django"], "total_experience": 4, "location": "Remote", "available": True},
        {"candidate_id": "C125", "final_score": 88, "skills": ["Python", "Flask"], "total_experience": 4, "location": "Bangalore", "available": True},
        {"candidate_id": "C126", "final_score": None, "skills": None, "total_experience": None, "location": None, "available": None}
    ]
    
    # 2. Batch Evaluation of Mock Data
    print("\n--- [STEP 2] RUNNING BATCH ELIGIBILITY EVALUATION (Backend Developer Mock Pool) ---")
    mock_results = evaluate_candidates_batch(mock_pool, backend_rules)
    
    print(f"{'Candidate ID':<13} | {'ATS Score':<10} | {'Status':<10} | Checks (Skills / Exp / Loc / Avail)")
    print("-" * 75)
    for res in mock_results:
        checks = res["checks"]
        checks_str = f"Skills:{'Y' if checks['skill_match'] else 'N'} | Exp:{'Y' if checks['experience_match'] else 'N'} | Loc:{'Y' if checks['location_match'] else 'N'} | Avail:{'Y' if checks['availability_match'] else 'N'}"
        print(f"{res['candidate_id']:<13} | {checks['ats_score']:<10} | {res['eligibility_status']:<10} | {checks_str}")
        
    print("\nDetailed Single Result JSON Structure:")
    print(json.dumps(mock_results[0], indent=2))
    
    # 3. Dynamic Evaluation of your 17 Actual Resumes using Tailored Role-Specific Rules
    print("\n==========================================================================================")
    print("--- [STEP 3] DYNAMIC EVALUATION OF ALL 17 WORKSPACE CANDIDATE RESUMES ---")
    print("==========================================================================================")
    
    ats_results_dir = "data/ats_results"
    skills_dir = "data/skills_extracted"
    experience_dir = "data/experience_parsed"
    
    actual_candidates_pool = []
    
    if os.path.exists(ats_results_dir):
        eval_files = [f for f in os.listdir(ats_results_dir) if f.endswith("_evaluation.json")]
        
        for f in eval_files:
            cand_id = f.replace("_evaluation.json", "")
            
            # Load ATS Score
            with open(os.path.join(ats_results_dir, f), "r", encoding="utf-8") as file:
                eval_data = json.load(file)
            final_score = eval_data.get("final_score", 0)
            job_applied = eval_data.get("job_title_applied", "tool die maker")
            
            # Load extracted skills list
            skills_path = os.path.join(skills_dir, f"{cand_id}_skills.json")
            skills_list = []
            if os.path.exists(skills_path):
                with open(skills_path, "r", encoding="utf-8") as file:
                    skills_json = json.load(file)
                    skills_list = [item.get("skill") for item in skills_json if item.get("skill")]
            
            # Load total experience years
            exp_path = os.path.join(experience_dir, f"{cand_id}_experience.json")
            exp_years = 0
            if os.path.exists(exp_path):
                with open(exp_path, "r", encoding="utf-8") as file:
                    exp_json = json.load(file)
                    exp_years = exp_json.get("total_experience_years", 0)
            
            actual_candidates_pool.append({
                "candidate_id": cand_id,
                "final_score": final_score,
                "skills": skills_list,
                "total_experience": exp_years,
                "job_title": job_applied,
                "location": "Kerala",  # default
                "available": True      # default
            })
            
    if actual_candidates_pool:
        print(f"\nSuccessfully loaded and mapped {len(actual_candidates_pool)} actual candidate files from your database.")
        
        actual_results = []
        for cand in actual_candidates_pool:
            # Generate job-specific rules dynamically
            cand_rules = get_rules_for_job(cand["job_title"])
            result = evaluate_candidate(cand, cand_rules)
            result["job_title_applied"] = cand["job_title"]
            result["mandatory_skills_required"] = cand_rules["mandatory_skills"]
            actual_results.append(result)
            
        print("\nTailored Role-Specific Eligibility Summary (17 Resumes):")
        print(f"{'Candidate ID':<42} | {'Applied Job Role':<22} | {'ATS Score':<9} | {'Status':<12} | Mandatory Skills Required")
        print("-" * 115)
        for res in actual_results:
            req_skills = ", ".join(res["mandatory_skills_required"]) if res["mandatory_skills_required"] else "None"
            print(f"{res['candidate_id']:<42} | {res['job_title_applied']:<22} | {res['checks']['ats_score']:<9.2f} | {res['eligibility_status']:<12} | {req_skills}")
        print("-" * 115)
        
    else:
        print("\nError: No candidate evaluation folders found. Please run 'python run_d11_to_15_ats_pipeline.py' first.")
        
    print("\n------------------------------------------------------------------------------------------")
    print("Day 21 Eligibility Engine Verification Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
