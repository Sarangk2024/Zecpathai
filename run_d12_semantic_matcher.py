# run_semantic_matcher.py - Standalone runner to check Day 12 (Semantic Matching Engine)

import os
import json
import sys
from ats_engine.semantic_matcher import match_resume_to_jd, classify_match
from ats_engine.experience_parser import extract_roles, determine_target_role
from parsers.section_classifier import detect_sections
from utils.logger import logger

def main():
    logger.info("Initializing Day 12 Semantic Matching Engine Check...")
    
    processed_resumes_dir = "data/processed_resumes"
    skills_dir = "data/skills_extracted"
    jds_dir = "data/processed_jds"
    output_dir = "data/semantic_matches"
    
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(processed_resumes_dir):
        print("Error: data/processed_resumes directory does not exist.")
        return
        
    resume_files = [f for f in os.listdir(processed_resumes_dir) if f.endswith(".txt")]
    jd_files = [f for f in os.listdir(jds_dir) if f.endswith(".json")]
    
    if not resume_files or not jd_files:
        print("Error: Missing resume or JD profiles. Make sure parsing is run first.")
        return
        
    # Load JDs
    jd_profiles = []
    for f in jd_files:
        with open(os.path.join(jds_dir, f), "r", encoding="utf-8") as file:
            jd_profiles.append(json.load(file))
            
    # Reference/default JD
    default_jd = jd_profiles[0]
    for jd in jd_profiles:
        if "tool" in jd.get("job_title", "").lower() and "die" in jd.get("job_title", "").lower():
            default_jd = jd
            break
            
    print("\n==========================================================================================")
    print("ZECPATH SEMANTIC MATCHING ENGINE RUNNER (DAY 12)")
    print("==========================================================================================")
    print(f"Resumes Input: {processed_resumes_dir}")
    print(f"JDs Input:     {jds_dir}")
    print(f"Output Folder: {output_dir}\n")
    
    print(f"{'Candidate Resume Filename':<48} | {'Matched JD Role':<24} | {'Skills Sim':<10} | {'Exp Sim':<8} | {'Proj Sim':<8} | {'Final Sim':<9} | {'Match Class'}")
    print("-" * 135)
    
    for file in resume_files:
        resume_name = file.replace("_cleaned.txt", "")
        resume_path = os.path.join(processed_resumes_dir, file)
        skills_path = os.path.join(skills_dir, f"{resume_name}_skills.json")
        
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
            
            is_mismatched = False
            if not matched_jd:
                matched_jd = default_jd
                is_mismatched = True
                
            # Load candidate skills
            candidate_skills = []
            if os.path.exists(skills_path):
                with open(skills_path, "r", encoding="utf-8") as sf:
                    skills_data = json.load(sf)
                    candidate_skills = [item.get("skill") for item in skills_data if item.get("skill")]
            
            # Format projects & experience blocks
            sections = detect_sections(content)
            projects_list = []
            for proj in sections.get("projects", []):
                if proj.strip():
                    projects_list.append({"name": proj[:30], "description": proj})
                    
            from ats_engine.experience_parser import extract_experience_blocks
            exp_text = "\n".join(sections.get("experience", []))
            experiences = extract_experience_blocks(exp_text)
            
            resume_obj = {
                "skills": candidate_skills,
                "experience": experiences,
                "projects": projects_list
            }
            
            # Semantic Matching
            match_results = match_resume_to_jd(resume_obj, matched_jd)
            final_similarity = match_results["final_similarity_score"]
            match_class = classify_match(final_similarity)
            
            # Save output JSON
            output_name = file.replace("_cleaned.txt", "_semantic_match.json")
            with open(os.path.join(output_dir, output_name), "w", encoding="utf-8") as out_f:
                json.dump({
                    "candidate_id": resume_name,
                    "target_jd": matched_jd.get("job_title"),
                    "is_mismatched_tech": is_mismatched,
                    "semantic_scores": match_results,
                    "match_classification": match_class
                }, out_f, indent=2)
                
            display_jd = matched_jd.get("job_title")
            if is_mismatched:
                display_jd = f"mismatch ({display_jd})"
                
            print(
                f"{file:<48} | {display_jd:<24} | "
                f"{match_results['skills_similarity']:<10.2f} | "
                f"{match_results['experience_similarity']:<8.2f} | "
                f"{match_results['project_similarity']:<8.2f} | "
                f"{final_similarity:<9.2f}% | {match_class}"
            )
            
        except Exception as e:
            print(f"{file:<48} | FAILED ({e})")
            
    print("\n------------------------------------------------------------------------------------------")
    print("Semantic Matching Engine Run Completed Successfully!")
    print(f"Structured outputs saved to: {os.path.abspath(output_dir)}")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
