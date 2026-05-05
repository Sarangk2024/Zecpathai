# run_skill_extractor.py - Batch skill extractor for candidate resumes.

import os
import json
from ats_engine.skill_extractor import extract_skills_with_confidence
from utils.logger import logger

def main():
    logger.info("Initializing Resume Skill Extractor Pipeline...")
    
    processed_dir = os.path.join("data", "processed_resumes")
    output_dir = os.path.join("data", "skills_extracted")
    
    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(processed_dir) if f.endswith(".txt")]
    
    if not files:
        print("No processed resumes found. Please run 'python run_parser.py' first.")
        return
        
    print("\n==========================================================================================")
    print("ZECPATH RESUME SKILL EXTRACTION BATCH RUNNER")
    print("==========================================================================================")
    print(f"Input Directory:  {processed_dir}")
    print(f"Output Directory: {output_dir}\n")
    
    # Print table header
    print(f"{'Candidate Resume Filename':<55} | {'Extracted Skills with Confidence (Descending)'}")
    print("-" * 125)
    
    for idx, file in enumerate(files, 1):
        input_path = os.path.join(processed_dir, file)
        output_name = file.replace("_cleaned.txt", "_skills.json")
        output_path = os.path.join(output_dir, output_name)
        
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            skills_data = extract_skills_with_confidence(content)
            
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(skills_data, out, indent=2)
            
            # Format skills for visual table
            skills_str = ", ".join([f"{item['skill']} ({item['confidence']})" for item in skills_data])
            if not skills_str:
                skills_str = "None matched"
                
            print(f"{file:<55} | {skills_str}")
        except Exception as e:
            print(f"{file:<55} | FAILED ({e})")
            
    print("\n------------------------------------------------------------------------------------------")
    print("Batch Skill Extraction Completed Successfully!")
    print(f"All structured JSON outputs saved to: {os.path.abspath(output_dir)}")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
