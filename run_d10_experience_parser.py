# run_experience_parser.py - Batch experience parser for candidate resumes.

import os
import json
import sys
from ats_engine.experience_parser import (
    extract_experience_blocks, extract_roles, calculate_total_experience,
    calculate_total_experience_months, detect_gaps, detect_overlaps, calculate_relevance,
    determine_target_role, load_jd_profiles, extract_education_max_year
)
from parsers.section_classifier import detect_sections
from utils.logger import logger

def main():
    logger.info("Initializing Resume Experience Parser Pipeline...")
    
    processed_dir = os.path.join("data", "processed_resumes")
    output_dir = os.path.join("data", "experience_parsed")
    
    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(processed_dir) if f.endswith(".txt")]
    
    if not files:
        print("No processed resumes found. Please run 'python run_parser.py' first.")
        return
        
    # Load all processed Job Descriptions
    jd_profiles = load_jd_profiles()
    
    print("\n==========================================================================================")
    print("ZECPATH RESUME EXPERIENCE PARSING BATCH RUNNER")
    print("==========================================================================================")
    print(f"Input Directory:  {processed_dir}")
    print(f"Output Directory: {output_dir}\n")
    
    # Print table header
    print(f"{'Candidate Resume Filename':<52} | {'Exp (Y)':<7} | {'Exp (M)':<7} | {'Relevance':<9} | {'Gaps?':<6} | {'Overlaps?':<9} | {'Extracted Companies'}")
    print("-" * 135)
    
    for idx, file in enumerate(files, 1):
        input_path = os.path.join(processed_dir, file)
        output_name = file.replace("_cleaned.txt", "_experience.json")
        output_path = os.path.join(output_dir, output_name)
        
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Classify sections and isolate experience
            sections = detect_sections(content)
            exp_text = "\n".join(sections.get("experience", []))
            
            experiences = extract_experience_blocks(exp_text)
            roles = extract_roles(content)
            total_exp = calculate_total_experience(experiences)
            total_exp_months = calculate_total_experience_months(experiences)
            
            max_edu_year = extract_education_max_year(content)
            gaps = detect_gaps(experiences, max_edu_year)
            overlaps = detect_overlaps(experiences)
            
            # Score relevance against dynamically matched JD
            target_role = determine_target_role(roles, file, jd_profiles)
            relevance = calculate_relevance(roles, target_role)
            
            # Add a baseline relevance of 10.0% if the candidate has a B.Tech/B.E engineering qualification
            has_btech = any(kw in content.lower() for kw in ["b.tech", "b.e", "b.e.", "bachelor of engineering", "bachelor of technology"])
            if relevance < 10.0 and has_btech:
                relevance = 10.0
            
            # Save JSON structure
            output_data = {
                "candidate_file": file,
                "extracted_experiences": experiences,
                "extracted_roles": roles,
                "total_experience_years": total_exp,
                "total_experience_months": total_exp_months,
                "detected_gaps": gaps,
                "detected_overlaps": [
                    [o[0]["company"], o[1]["company"]] for o in overlaps
                ],
                "target_job_role": target_role,
                "role_relevance_score": relevance
            }
            
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(output_data, out, indent=2)
            
            # Format display strings
            gaps_str = "YES" if gaps else "NO"
            overlaps_str = "YES" if overlaps else "NO"
            companies_str = ", ".join([exp["company"] for exp in experiences])
            if not companies_str:
                companies_str = "None (Entry-Level)"
                
            print(f"{file:<52} | {total_exp:<7} | {total_exp_months:<7} | {relevance:<9.1f}% | {gaps_str:<6} | {overlaps_str:<9} | {companies_str}")
        except Exception as e:
            print(f"{file:<52} | FAILED ({e})")
            
    print("\n------------------------------------------------------------------------------------------")
    print("Batch Experience Parsing Completed Successfully!")
    print(f"All structured JSON outputs saved to: {os.path.abspath(output_dir)}")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
