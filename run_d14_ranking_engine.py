# run_ranking_engine.py - Standalone runner to check Day 14 (Ranking Engine)

import os
import json
import sys
from ats_engine.ranking_engine import ranking_pipeline, format_recruiter_summary
from utils.logger import logger

def main():
    logger.info("Initializing Day 14 Ranking Engine Check...")
    
    scores_dir = "data/ats_scores"
    output_dir = "data/ats_rankings"
    
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(scores_dir) or not os.listdir(scores_dir):
        print("Note: run_ats_scorer.py outputs not found. Running ATS scorer first...")
        from run_ats_scorer import main as run_scorer
        run_scorer()
        
    score_files = [f for f in os.listdir(scores_dir) if f.endswith(".json")]
    
    candidates = []
    for f in score_files:
        with open(os.path.join(scores_dir, f), "r", encoding="utf-8") as file:
            score_data = json.load(file)
            candidates.append({
                "candidate_id": score_data.get("candidate_id"),
                "final_score": score_data.get("final_score"),
                "skill_score": score_data.get("breakdown", {}).get("skill_score"),
                "experience_score": score_data.get("breakdown", {}).get("experience_score"),
                "education_score": score_data.get("breakdown", {}).get("education_score"),
                "semantic_score": score_data.get("breakdown", {}).get("semantic_score")
            })
            
    print("\n==========================================================================================")
    print("ZECPATH CANDIDATE RANKING ENGINE RUNNER (DAY 14)")
    print("==========================================================================================")
    print(f"Scores Input: {scores_dir}")
    print(f"Output Folder: {output_dir}\n")
    
    pipeline_results = ranking_pipeline(candidates)
    ranked_list = pipeline_results["ranked_list"]
    top_candidates = pipeline_results["top_candidates"]
    
    print(f"{'Rank':<5} | {'Candidate Resume Filename':<52} | {'ATS Score':<9} | {'Status':<12}")
    print("-" * 90)
    
    for c in ranked_list:
        print(
            f"{c['rank']:<5} | {c['candidate_id'] + '_cleaned.txt':<52} | "
            f"{c['final_score']:<9.2f} | {c['status']:<12}"
        )
        
    recruiter_sum = format_recruiter_summary("BATCH_01", ranked_list)
    
    with open(os.path.join(output_dir, "ranked_candidates.json"), "w", encoding="utf-8") as out_f:
        json.dump({
            "ranked_list": ranked_list,
            "top_candidates": top_candidates,
            "recruiter_summary": recruiter_sum
        }, out_f, indent=2)
        
    print("\n------------------------------------------------------------------------------------------")
    print("RECRUITER DASHBOARD SUMMARY")
    print("------------------------------------------------------------------------------------------")
    print(f"Total Evaluated: {recruiter_sum['summary']['total_candidates']}")
    print(f"Shortlisted:      {recruiter_sum['summary']['shortlisted']}")
    print(f"Under Review:     {recruiter_sum['summary']['review']}")
    print(f"Rejected:         {recruiter_sum['summary']['rejected']}")
    print(f"All ranking results saved to: {os.path.abspath(output_dir)}")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
