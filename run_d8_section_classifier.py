# run_section_classifier.py - Batch segmenter for candidate resumes.

import os
import json
from parsers.section_classifier import detect_sections
from utils.logger import logger

def main():
    logger.info("Initializing Resume Section Classifier Pipeline...")
    
    processed_dir = os.path.join("data", "processed_resumes")
    output_dir = os.path.join("data", "segmented_resumes")
    
    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(processed_dir) if f.endswith(".txt")]
    
    if not files:
        print("No processed resumes found. Please run 'python run_parser.py' first.")
        return
        
    print("\n==================================================")
    print("ZECPATH RESUME SECTION SEGMENTATION BATCH RUNNER")
    print("==================================================")
    print(f"Input Directory:  {processed_dir}")
    print(f"Output Directory: {output_dir}\n")
    
    for idx, file in enumerate(files, 1):
        input_path = os.path.join(processed_dir, file)
        output_name = file.replace("_cleaned.txt", "_segmented.json")
        output_path = os.path.join(output_dir, output_name)
        
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            segmented = detect_sections(content)
            
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(segmented, out, indent=2)
                
            print(f"  [{idx}/{len(files)}] {file} ... SUCCESS")
        except Exception as e:
            print(f"  [{idx}/{len(files)}] {file} ... FAILED ({e})")
            
    print("\n--------------------------------------------------")
    print("Batch Segmentation Completed Successfully!")
    print(f"All outputs saved to: {os.path.abspath(output_dir)}")
    print("==================================================\n")

if __name__ == "__main__":
    main()
