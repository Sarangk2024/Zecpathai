# run_ats_scorer.py - Standalone runner to check Day 13 (ATS Scoring Formula Design)

import os
import json
import sys
from ats_engine.ats_scorer import generate_candidate_score
from ats_engine.experience_parser import extract_roles, determine_target_role
from parsers.education_parser import extract_education, calculate_education_relevance, DEGREE_MAP
from utils.logger import logger

def calculate_skill_score(candidate_skills, jd_skills):
    if not jd_skills:
        return 0.0
    matched = set(s.lower().replace("_", " ") for s in candidate_skills).intersection(
        set(s.lower().replace("_", " ") for s in jd_skills)
    )
    return round((len(matched) / len(jd_skills)) * 100.0, 2)

def main():
    logger.info("Initializing Day 13 ATS Scorer Check...")
    
    processed_resumes_dir = "data/processed_resumes"
    skills_dir = "data/skills_extracted"
    jds_dir = "data/processed_jds"
    semantic_dir = "data/semantic_matches"
    output_dir = "data/ats_scores"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Run dependencies check
    if not os.path.exists(semantic_dir) or not os.listdir(semantic_dir):
        print("Note: run_semantic_matcher.py outputs not found. Running semantic matcher first...")
        from run_semantic_matcher import main as run_sem
        run_sem()
        
    resume_files = [f for f in os.listdir(processed_resumes_dir) if f.endswith(".txt")]
    jd_files = [f for f in os.listdir(jds_dir) if f.endswith(".json")]
    
    # Load JDs
    jd_profiles = []
    for f in jd_files:
        with open(os.path.join(jds_dir, f), "r", encoding="utf-8") as file:
            jd_profiles.append(json.load(file))
            
    # Reference JD
    default_jd = jd_profiles[0]
    for jd in jd_profiles:
        if "tool" in jd.get("job_title", "").lower() and "die" in jd.get("job_title", "").lower():
            default_jd = jd
            break
            
    print("\n==========================================================================================")
    print("ZECPATH ATS SCORING ENGINE RUNNER (DAY 13)")
    print("==========================================================================================")
    print(f"Resumes Input: {processed_resumes_dir}")
    print(f"Output Folder: {output_dir}\n")
    
    print(f"{'Candidate Resume Filename':<48} | {'Weights Used (S/Exp/Ed/Sem)':<30} | {'Skill%':<6} | {'Exp%':<6} | {'Edu%':<6} | {'Sem%':<6} | {'Final ATS Score'}")
    print("-" * 135)
    
    for file in resume_files:
        resume_name = file.replace("_cleaned.txt", "")
        resume_path = os.path.join(processed_resumes_dir, file)
        skills_path = os.path.join(skills_dir, f"{resume_name}_skills.json")
        sem_path = os.path.join(semantic_dir, f"{resume_name}_semantic_match.json")
        
        try:
            with open(resume_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Determine target role
            roles = extract_roles(content)
            target_role = determine_target_role(roles, file, jd_profiles)
            
            matched_jd = None
            if target_role != "unknown":
                for jd in jd_profiles:
                    if jd.get("job_title", "").lower().strip() == target_role.lower().strip():
                        matched_jd = jd
                        break
            
            if not matched_jd:
                matched_jd = default_jd
                
            # 1. Skill Score
            candidate_skills = []
            if os.path.exists(skills_path):
                with open(skills_path, "r", encoding="utf-8") as sf:
                    skills_data = json.load(sf)
                    candidate_skills = [item.get("skill") for item in skills_data if item.get("skill")]
            skill_score = calculate_skill_score(candidate_skills, matched_jd.get("required_skills", []))
            
            # 2. Experience Score
            from ats_engine.experience_parser import calculate_relevance
            exp_score = calculate_relevance(roles, target_role)
            has_btech = any(kw in content.lower() for kw in ["b.tech", "b.e", "b.e.", "bachelor of engineering", "bachelor of technology"])
            if exp_score < 10.0 and has_btech:
                exp_score = 10.0
                
            # 3. Education Score
            education_list = extract_education(content)
            candidate_degree = education_list[0]["degree"] if education_list else "None"
            req_degree = matched_jd.get("education_required", "")
            req_degree_normalized = "B.Tech"
            for deg in ["diploma", "iti", "b.tech", "b.e", "m.tech", "mba", "bsc", "msc"]:
                if deg in req_degree.lower():
                    req_degree_normalized = DEGREE_MAP.get(deg.replace(".", ""), deg.title())
                    break
            education_relevance = calculate_education_relevance(candidate_degree, req_degree_normalized) * 100.0
            
            # 4. Semantic Score
            semantic_score = 0.0
            if os.path.exists(sem_path):
                with open(sem_path, "r", encoding="utf-8") as sem_f:
                    sem_data = json.load(sem_f)
                    semantic_score = sem_data.get("semantic_scores", {}).get("final_similarity_score", 0.0)
                    
            cand_score_input = {
                "candidate_id": resume_name,
                "skill_score": skill_score,
                "experience_score": exp_score,
                "education_score": education_relevance,
                "semantic_score": semantic_score
            }
            
            # Call ATS Scorer
            score_data = generate_candidate_score(cand_score_input, matched_jd)
            final_score = score_data["final_score"]
            w = score_data["weights_used"]
            
            # Save Output JSON
            output_name = file.replace("_cleaned.txt", "_ats_score.json")
            with open(os.path.join(output_dir, output_name), "w", encoding="utf-8") as out_f:
                json.dump(score_data, out_f, indent=2)
                
            w_str = f"S:{w['skills']:.2f}/X:{w['experience']:.2f}/Ed:{w['education']:.2f}/Sm:{w['semantic']:.2f}"
            print(
                f"{file:<48} | {w_str:<30} | "
                f"{skill_score:<6.1f} | {exp_score:<6.1f} | {education_relevance:<6.1f} | {semantic_score:<6.1f} | {final_score:<15.2f}"
            )
        except Exception as e:
            print(f"{file:<48} | FAILED ({e})")
            
    print("\n------------------------------------------------------------------------------------------")
    print("ATS Scoring Run Completed Successfully!")
    print(f"Structured outputs saved to: {os.path.abspath(output_dir)}")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
