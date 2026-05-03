# run_parser.py - Batch execution script for Zecpath AI resume extraction.

import os
from parsers.resume_extractor import extract_resume, save_cleaned_text
from utils.logger import logger

def main():
    logger.info("Initializing Zecpath AI Pipeline Batch Run...")
    
    resumes_dir = os.path.join("data", "resumes")
    processed_dir = os.path.join("data", "processed_resumes")
    
    os.makedirs(resumes_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    
    try:
        # Check files in directory
        files = [f for f in os.listdir(resumes_dir) if f.split(".")[-1].lower() in ["pdf", "docx", "doc"]]
        
        if not files:
            print("\n==================================================")
            print("ZECPATH AI PIPELINE BATCH RUNNER")
            print("==================================================")
            print("No resumes found inside data/resumes/ folder.")
            print("\nTo test the parser, you can:")
            print("1. Place your own PDF or DOCX resume in data/resumes/")
            print("2. Run the mock resume generator to populate samples:")
            print("   python -m utils.generate_resumes")
            print("==================================================\n")
            logger.warning("No resumes found to process during pipeline run.")
            return

        print("\n==================================================")
        print("ZECPATH RESUME TEXT EXTRACTION BATCH PIPELINE")
        print("==================================================")
        print(f"Input Directory:  {resumes_dir}")
        print(f"Output Directory: {processed_dir}\n")
        print("Scanning files...")
        print(f"Found {len(files)} resumes to process.\n")
        print("Processing:")
        
        processed_count = 0
        failed_count = 0
        
        for idx, file in enumerate(files, 1):
            input_path = os.path.join(resumes_dir, file)
            output_name = file.rsplit(".", 1)[0] + "_cleaned.txt"
            output_path = os.path.join(processed_dir, output_name)
            
            try:
                result = extract_resume(input_path)
                save_cleaned_text(output_path, result)
                print(f"  [{idx}/{len(files)}] {file} ... SUCCESS")
                processed_count += 1
            except Exception as fe:
                logger.error(f"Failed to process {file}: {str(fe)}")
                print(f"  [{idx}/{len(files)}] {file} ... FAILED")
                failed_count += 1
            
        print("\n--------------------------------------------------")
        print("Pipeline Batch Run Completed")
        print("--------------------------------------------------")
        print(f"Total Resumes Scanned:   {len(files)}")
        print(f"Successfully Processed:  {processed_count}")
        print(f"Failed to Process:       {failed_count}")
        print(f"\nAll parsed output text files are stored in:")
        print(f"-> {os.path.abspath(processed_dir)}")
        print("==================================================\n")
        logger.info(f"Pipeline finished. Successfully processed {processed_count} files, failed {failed_count} files.")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        print(f"An error occurred during pipeline execution: {e}")

if __name__ == "__main__":
    main()
