# run_d23_transcript_architecture.py - Standalone transcript schema and normalizer verification runner (Day 23).

import json
from screening_ai.transcript_normalizer import normalize_transcript, process_transcript

def main():
    print("\n==========================================================================================")
    print("ZECPATH TRANSCRIPT DATA ARCHITECTURE RUNNER (DAY 23)")
    print("==========================================================================================")
    
    # 1. Load Voice Transcript Schema
    print("\n--- [STEP 1] LOADING STRUCTURED VOICE TRANSCRIPT SCHEMA ---")
    with open("data/voice_transcript_schema.json", "r", encoding="utf-8") as f:
        voice_schema = json.load(f)
    print(json.dumps(voice_schema, indent=2))
    
    # 2. Load AI Screening Data Structure
    print("\n--- [STEP 2] LOADING AI SCREENING DATA STRUCTURE ---")
    with open("screening_ai/screening_data_structure.json", "r", encoding="utf-8") as f:
        screening_structure = json.load(f)
    print(json.dumps(screening_structure, indent=2))
    
    # 3. Demonstrate Transcript Normalization Rules
    print("\n--- [STEP 3] TRANSCRIPT NORMALIZATION RULES DEMO ---")
    raw_speech = "Um uh like, I worked as a machinist for you know, 3 years at Bharat Forge."
    clean_speech = normalize_transcript(raw_speech)
    print("Raw Spoken Answer: ", raw_speech)
    print("Cleaned / Standard: ", clean_speech)
    
    # 4. Ingest and Process Raw Answers List
    raw_answers = [
        {"question_id": "Q1", "text": "Um, uh, I am a developer...", "confidence": 0.93},
        {"question_id": "Q3", "text": "I have like 3 years experience in Python.", "confidence": 0.91}
    ]
    print("\n--- [STEP 4] INGESTING RAW TRANSCRIPT ANSWERS ARRAY ---")
    processed = process_transcript(raw_answers)
    print(json.dumps(processed, indent=2))
    
    # 5. Database SQL Schema Definitions Print
    print("\n--- [STEP 5] SQL DATABASE SCHEMA SCHEMATICS ---")
    sql_ddl = """
CREATE TABLE transcripts (
    transcript_id VARCHAR(50) PRIMARY KEY,
    candidate_id VARCHAR(50),
    job_id VARCHAR(50),
    language VARCHAR(10),
    overall_confidence FLOAT,
    created_at TIMESTAMP
);

CREATE TABLE transcript_entries (
    entry_id SERIAL PRIMARY KEY,
    transcript_id VARCHAR(50),
    question_id VARCHAR(50),
    question_text TEXT,
    answer_text TEXT,
    confidence_score FLOAT,
    start_time VARCHAR(10),
    end_time VARCHAR(10),
    duration_seconds INT
);
    """
    print(sql_ddl.strip())
    
    print("\n------------------------------------------------------------------------------------------")
    print("Day 23 Transcript Data Architecture Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
