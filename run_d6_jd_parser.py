# run_jd_parser.py - Batch execution script for Zecpath AI job description parsing.

import os
import json
from parsers.jd_parser import parse_job_description
from utils.logger import logger

def main():
    logger.info("Initializing Zecpath AI Job Description Pipeline Batch Run...")
    
    jds_dir = os.path.join("data", "jd")
    processed_jds_dir = os.path.join("data", "processed_jds")
    
    os.makedirs(jds_dir, exist_ok=True)
    os.makedirs(processed_jds_dir, exist_ok=True)
    
    try:
        # Check files in input directory
        files = [f for f in os.listdir(jds_dir) if f.endswith(".txt")]
        
        if not files:
            print("\n==================================================")
            print("ZECPATH AI JD PIPELINE BATCH RUNNER")
            print("==================================================")
            print("No job descriptions found inside data/jd/ folder.")
            print("\nTo generate the split JDs, please run:")
            print("  python -m utils.split_jds")
            print("==================================================\n")
            logger.warning("No job descriptions found to process during pipeline run.")
            return

        print("\n==================================================")
        print("ZECPATH JOB DESCRIPTION BATCH PARSER PIPELINE")
        print("==================================================")
        print(f"Input Directory:  {jds_dir}")
        print(f"Output Directory: {processed_jds_dir}\n")
        print("Scanning files...")
        print(f"Found {len(files)} job descriptions to process.\n")
        print("Processing:")
        
        processed_count = 0
        failed_count = 0
        
        for idx, file in enumerate(files, 1):
            input_path = os.path.join(jds_dir, file)
            output_name = file.rsplit(".", 1)[0] + "_profile.json"
            output_path = os.path.join(processed_jds_dir, output_name)
            
            try:
                with open(input_path, "r", encoding="utf-8") as f:
                    jd_content = f.read()
                
                result = parse_job_description(jd_content)
                
                # Write parsed structured object to output folder
                with open(output_path, "w", encoding="utf-8") as out:
                    json.dump(result, out, indent=2)
                    
                print(f"  [{idx}/{len(files)}] {file} ... SUCCESS")
                processed_count += 1
            except Exception as fe:
                logger.error(f"Failed to process {file}: {str(fe)}")
                print(f"  [{idx}/{len(files)}] {file} ... FAILED")
                failed_count += 1
            
        print("\n--------------------------------------------------")
        print("Pipeline JD Batch Run Completed")
        print("--------------------------------------------------")
        print(f"Total JDs Scanned:      {len(files)}")
        print(f"Successfully Parsed:    {processed_count}")
        print(f"Failed to Process:      {failed_count}")
        print(f"\nAll structured JD JSON profiles are stored in:")
        print(f"-> {os.path.abspath(processed_jds_dir)}")
        print("==================================================\n")
        logger.info(f"JD Pipeline finished. Successfully processed {processed_count} JDs, failed {failed_count} JDs.")
        
    except Exception as e:
        logger.error(f"JD Pipeline execution failed: {str(e)}")
        print(f"An error occurred during JD pipeline execution: {e}")

if __name__ == "__main__":
    main()
