# run_education_parser.py - Batch education and certification parser for candidate resumes.

import os
import json
import sys
from parsers.education_parser import (
    extract_education, extract_certifications, generate_academic_profile
)
from utils.logger import logger

def main():
    logger.info("Initializing Resume Education & Certification Parser Pipeline...")
    
    processed_dir = os.path.join("data", "processed_resumes")
    output_dir = os.path.join("data", "education_parsed")
    
    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(processed_dir) if f.endswith(".txt")]
    
    if not files:
        print("No processed resumes found. Please run 'python run_parser.py' first.")
        return
        
    print("\n==========================================================================================")
    print("ZECPATH RESUME EDUCATION & CERTIFICATION PARSING BATCH RUNNER")
    print("==========================================================================================")
    print(f"Input Directory:  {processed_dir}")
    print(f"Output Directory: {output_dir}\n")
    
    # Print table header
    print(f"{'Candidate Resume Filename':<52} | {'Degree':<10} | {'Field of Study':<22} | {'Grad Year':<9} | {'Certifications (Category)'}")
    print("-" * 140)
    
    for idx, file in enumerate(files, 1):
        input_path = os.path.join(processed_dir, file)
        output_name = file.replace("_cleaned.txt", "_education.json")
        output_path = os.path.join(output_dir, output_name)
        
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Parse education and certifications
            education_list = extract_education(content)
            certifications_list = extract_certifications(content)
            
            # Generate structured profile
            candidate_id = file.replace("_cleaned.txt", "")
            academic_profile = generate_academic_profile(candidate_id, content)
            
            # Save JSON structure
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(academic_profile, out, indent=2)
            
            # Format display strings for the table
            if education_list:
                primary_edu = education_list[0]
                degree_str = primary_edu.get("degree", "None")
                field_str = primary_edu.get("field", "Not Specified")
                year_str = primary_edu.get("year_of_completion") or "N/A"
            else:
                degree_str = "None"
                field_str = "Not Specified"
                year_str = "N/A"
                
            if len(education_list) > 1:
                degree_str += f" (+{len(education_list)-1})"
                
            certs_str = ", ".join([f"{c['name']} ({c['category']})" for c in certifications_list])
            if not certs_str:
                certs_str = "None"
                
            if len(field_str) > 20:
                field_str = field_str[:17] + "..."
            if len(certs_str) > 35:
                certs_str = certs_str[:32] + "..."
                
            print(f"{file:<52} | {degree_str:<10} | {field_str:<22} | {year_str:<9} | {certs_str}")
        except Exception as e:
            print(f"{file:<52} | FAILED ({e})")
            
    print("\n------------------------------------------------------------------------------------------")
    print("Batch Education & Certification Parsing Completed Successfully!")
    print(f"All structured JSON outputs saved to: {os.path.abspath(output_dir)}")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
