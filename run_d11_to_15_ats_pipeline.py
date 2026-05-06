# run_ats_pipeline.py - Zecpath AI End-to-End ATS Pipeline Batch Runner

import os
import json
import re
import sys

# Ensure root directory is in sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from parsers.section_classifier import detect_sections
from parsers.education_parser import (
    extract_education, extract_certifications, 
    calculate_education_relevance, calculate_certification_relevance,
    generate_academic_profile, DEGREE_MAP
)
from ats_engine.experience_parser import (
    extract_experience_blocks, extract_roles, calculate_total_experience,
    calculate_total_experience_months, detect_gaps, detect_overlaps,
    determine_target_role, calculate_relevance, extract_education_max_year
)
from ats_engine.semantic_matcher import match_resume_to_jd, classify_match
from ats_engine.ats_scorer import generate_candidate_score, safe_score
from ats_engine.ranking_engine import ranking_pipeline, format_recruiter_summary
from ats_engine.fairness_engine import normalize_scores, mask_sensitive_data, generate_fair_score

def calculate_skill_score(candidate_skills, jd_skills):
    if not jd_skills:
        return 0.0
    matched = set(s.lower().replace("_", " ") for s in candidate_skills).intersection(
        set(s.lower().replace("_", " ") for s in jd_skills)
    )
    return round((len(matched) / len(jd_skills)) * 100.0, 2)

def main():
    print("\n==========================================================================================")
    print("ZECPATH AI ATS PIPELINE BATCH RUNNER (DAYS 11-15)")
    print("==========================================================================================\n")
    
    processed_resumes_dir = "data/processed_resumes"
    skills_dir = "data/skills_extracted"
    jds_dir = "data/processed_jds"
    output_dir = "data/ats_results"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Check inputs
    if not os.path.exists(processed_resumes_dir):
        print(f"Error: {processed_resumes_dir} directory does not exist. Run parsing scripts first.")
        return
        
    resume_files = [f for f in os.listdir(processed_resumes_dir) if f.endswith(".txt")]
    if not resume_files:
        print("Error: No processed resumes found.")
        return
        
    jd_files = [f for f in os.listdir(jds_dir) if f.endswith(".json")]
    if not jd_files:
        print("Error: No processed JDs found.")
        return
        
    # Load JDs
    jd_profiles = []
    for f in jd_files:
        with open(os.path.join(jds_dir, f), "r", encoding="utf-8") as file:
            jd_profiles.append(json.load(file))
            
    # Default Reference JD (e.g. Trainee Tool & Die Maker)
    default_jd = jd_profiles[0]
    for jd in jd_profiles:
        if "trainee" in jd.get("job_title", "").lower() and "tool" in jd.get("job_title", "").lower():
            default_jd = jd
            break
            
    print(f"Loaded {len(resume_files)} candidate resumes.")
    print(f"Loaded {len(jd_profiles)} Job Descriptions (JDs).")
    print(f"Using '{default_jd.get('job_title')}' as reference JD for mismatched tech candidates.\n")
    
    candidates_pool = []
    
    for idx, file in enumerate(resume_files, 1):
        resume_name = file.replace("_cleaned.txt", "")
        resume_path = os.path.join(processed_resumes_dir, file)
        skills_path = os.path.join(skills_dir, f"{resume_name}_skills.json")
        
        try:
            # 1. Read Resume Text
            with open(resume_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # 2. Extract Candidate Roles
            roles = extract_roles(content)
            
            # 3. Determine Matched Job Title from Library
            target_role = determine_target_role(roles, file, jd_profiles)
            
            # Find the actual JD profile matching this target_role
            matched_jd = None
            if target_role != "unknown":
                for jd in jd_profiles:
                    if jd.get("job_title", "").lower().strip() == target_role.lower().strip():
                        matched_jd = jd
                        break
            
            is_mismatched_tech = False
            if not matched_jd:
                matched_jd = default_jd
                is_mismatched_tech = (target_role == "unknown")
                
            # 4. Extract Education and Calculate Relevance
            education_list = extract_education(content)
            candidate_degree = education_list[0]["degree"] if education_list else "None"
            
            # Standardize JD required degree
            req_degree = matched_jd.get("education_required", "")
            req_degree_normalized = "B.Tech"
            for deg in ["diploma", "iti", "b.tech", "b.e", "m.tech", "mba", "bsc", "msc"]:
                if deg in req_degree.lower():
                    req_degree_normalized = DEGREE_MAP.get(deg.replace(".", ""), deg.title())
                    break
            education_relevance = calculate_education_relevance(candidate_degree, req_degree_normalized) * 100.0
            
            # 5. Load Extracted Skills & Calculate Skill Score
            candidate_skills = []
            if os.path.exists(skills_path):
                with open(skills_path, "r", encoding="utf-8") as sf:
                    skills_data = json.load(sf)
                    candidate_skills = [item.get("skill") for item in skills_data if item.get("skill")]
            
            jd_skills = matched_jd.get("required_skills", [])
            skill_score = calculate_skill_score(candidate_skills, jd_skills)
            
            # 6. Parse Experiences & Calculate Role Experience Score
            sections = detect_sections(content)
            exp_text = "\n".join(sections.get("experience", []))
            experiences = extract_experience_blocks(exp_text)
            
            # Experience score calculation
            exp_score = calculate_relevance(roles, target_role)
            # Add B.Tech baseline relevance check
            has_btech = any(kw in content.lower() for kw in ["b.tech", "b.e", "b.e.", "bachelor of engineering", "bachelor of technology"])
            if exp_score < 10.0 and has_btech:
                exp_score = 10.0
                
            # 7. Format Projects & Calculate Semantic Similarity
            projects_list = []
            for proj in sections.get("projects", []):
                if proj.strip():
                    projects_list.append({"name": proj[:30], "description": proj})
            
            resume_obj = {
                "skills": candidate_skills,
                "experience": experiences,
                "projects": projects_list
            }
            
            semantic_results = match_resume_to_jd(resume_obj, matched_jd)
            semantic_score = semantic_results["final_similarity_score"]
            
            # Override semantic score if it is a mismatched tech candidate to show the true misfit
            if is_mismatched_tech:
                # Software developer compared to Tool & Die Maker has very low semantic fit
                # Let's let the actual matcher run, which will yield a low score.
                pass
                
            # 8. Score Candidate using ATS Scorer
            cand_score_input = {
                "candidate_id": resume_name,
                "skill_score": skill_score,
                "experience_score": exp_score,
                "education_score": education_relevance,
                "semantic_score": semantic_score
            }
            
            score_data = generate_candidate_score(cand_score_input, matched_jd)
            final_score = score_data["final_score"]
            
            # Apply fairness adjustments (fair_score blending keyword & semantic)
            score_data_fair = generate_fair_score(cand_score_input)
            fair_score = score_data_fair["fair_score"]
            
            # Save raw candidate info in pool list
            candidates_pool.append({
                "candidate_id": resume_name,
                "filename": file,
                "job_title_applied": matched_jd.get("job_title"),
                "is_tech_mismatch": is_mismatched_tech,
                "skill_score": skill_score,
                "experience_score": exp_score,
                "education_score": education_relevance,
                "semantic_score": semantic_score,
                "final_score": final_score,
                "fair_score": fair_score,
                "masked_profile": mask_sensitive_data({
                    "name": resume_name.replace("_cleaned", "").replace("_", " "),
                    "gender": "Male" if "Sarang" in resume_name else "Not Specified",
                    "location": "Kerala" if "Sarang" in resume_name else "India",
                    "email": f"{resume_name.lower()}@example.com"
                })
            })
            
        except Exception as e:
            print(f"Failed to process {file}: {e}")
            import traceback
            traceback.print_exc()

    # 9. Apply Pool-Wide Normalization
    candidates_pool = normalize_scores(candidates_pool)
    
    # 10. Rank and Classify Candidates using Ranking Pipeline
    pipeline_results = ranking_pipeline(candidates_pool)
    ranked_list = pipeline_results["ranked_list"]
    top_candidates = pipeline_results["top_candidates"]
    
    # 11. Write structured results
    with open(os.path.join(output_dir, "ats_batch_results.json"), "w", encoding="utf-8") as out_f:
        json.dump({
            "ranked_candidates": ranked_list,
            "top_candidates": top_candidates,
            "summary": format_recruiter_summary("BATCH_01", ranked_list)
        }, out_f, indent=2)
        
    for c in ranked_list:
        c_name = c["candidate_id"]
        with open(os.path.join(output_dir, f"{c_name}_evaluation.json"), "w", encoding="utf-8") as out_c:
            json.dump(c, out_c, indent=2)
            
    # 12. Output Recruiters Summary Table
    print("-" * 155)
    print(f"{'Rank':<5} | {'Candidate Resume Filename':<52} | {'Matched JD Role':<28} | {'ATS Score':<9} | {'Fair Score':<10} | {'Status':<12} | {'Masked Profile Name'}")
    print("-" * 155)
    
    for c in ranked_list:
        display_jd = c["job_title_applied"]
        if c["is_tech_mismatch"]:
            display_jd = f"mismatch ({display_jd})"
            
        # PII mask check
        masked_name = c["masked_profile"].get("name", "MASKED")
        
        print(
            f"{c['rank']:<5} | {c['candidate_id'] + '_cleaned.txt':<52} | {display_jd:<28} | "
            f"{c['final_score']:<9.2f} | {c['fair_score']:<10.2f} | {c['status']:<12} | {masked_name}"
        )
    print("-" * 155)
    
    recruiter_sum = format_recruiter_summary("BATCH_01", ranked_list)
    print("\n==========================================================================================")
    print("BATCH RUN RECRUITER SUMMARY")
    print("==========================================================================================")
    print(f"Total Applicants Evaluated: {recruiter_sum['summary']['total_candidates']}")
    print(f"Shortlisted Candidates (Score >= 75): {recruiter_sum['summary']['shortlisted']}")
    print(f"Candidates under Review (Score 50-74): {recruiter_sum['summary']['review']}")
    print(f"Rejected Candidates (Score < 50):    {recruiter_sum['summary']['rejected']}")
    print("Structured outputs and individual JSONs saved to: data/ats_results/")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
