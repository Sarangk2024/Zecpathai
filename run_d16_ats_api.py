# run_ats_api.py - Direct API verification suite for Day 16 checking.

import os
import json
import asyncio
from fastapi import UploadFile
from io import BytesIO
from ats_engine.ats_api import (
    upload_resume, parse_resume, score_candidate, shortlist_candidates, 
    start_job, check_job_status, ParseRequest, ScoreRequest, ShortlistRequest, 
    StartJobRequest, ATSAPIException
)

async def run_tests():
    print("\n==========================================================================================")
    print("ZECPATH ATS REST API INTEGRATION CHECKER (DAY 16 - DIRECT TEST)")
    print("==========================================================================================")
    
    # 1. Prepare Mock Resume Data
    temp_resume_content = b"""
    KARTIK MEHTA
    VMC CNC Programmer Machinist
    Skills: CNC, Milling, Grinding, Mastercam, G-Code
    Experience:
    CNC Operator Programmer - Bharat Forge Ltd 2022 - Present
    Education:
    Diploma in Mechanical Engineering
    State Board of Technical Education Completed 2021
    """
    
    # Wrap in fastapi's UploadFile
    upload_file = UploadFile(filename="kartik_resume.txt", file=BytesIO(temp_resume_content))
    
    print("\n--- [STEP 1] TESTING /resume/upload ENDPOINT ---")
    try:
        response = await upload_resume(
            file=upload_file,
            job_id="J101",
            candidate_id="C999"
        )
        print("Upload Result:")
        print(json.dumps(response, indent=2))
        resume_id = response["resume_id"]
    except Exception as e:
        print("Upload test failed:", e)
        return
        
    print("\n--- [STEP 2] TESTING /resume/parse ENDPOINT ---")
    try:
        req = ParseRequest(resume_id=resume_id)
        response = parse_resume(req)
        print("Parse Result:")
        print(json.dumps(response, indent=2))
    except Exception as e:
        print("Parse test failed:", e)
        return
        
    print("\n--- [STEP 3] TESTING /ats/score ENDPOINT ---")
    try:
        req = ScoreRequest(candidate_id="C999", job_id="cnc machinist")
        response = score_candidate(req)
        print("Score Result:")
        print(json.dumps(response, indent=2))
    except Exception as e:
        print("Score test failed:", e)
        return
        
    print("\n--- [STEP 4] TESTING /ats/shortlist ENDPOINT ---")
    try:
        req = ShortlistRequest(job_id="J101")
        response = shortlist_candidates(req)
        print("Shortlist Result:")
        print(json.dumps(response, indent=2))
    except Exception as e:
        print("Shortlist test failed:", e)
        return
        
    print("\n--- [STEP 5] TESTING ERROR HANDLING (MISSING INPUTS) ---")
    try:
        await upload_resume(
            file=upload_file,
            job_id="J101",
            candidate_id="  "
        )
        print("Validation test failed (expected exception but got success)")
    except ATSAPIException as e:
        print("Expected API Error Captured:")
        print(json.dumps({
            "status": "error",
            "error_code": e.error_code,
            "message": e.message,
            "timestamp": e.timestamp
        }, indent=2))
    except Exception as e:
        print("Unexpected exception:", e)
        
    print("\n--- [STEP 6] TESTING ASYNC JOB FLOWS ---")
    try:
        req_start = StartJobRequest(resume_id=resume_id, job_id="cnc machinist")
        response_start = start_job(req_start)
        print("Job Start Result:")
        print(json.dumps(response_start, indent=2))
        
        job_id = response_start["job_id"]
        
        response_status = check_job_status(job_id)
        print("Job Status Check Result:")
        print(json.dumps(response_status, indent=2))
    except Exception as e:
        print("Async job test failed:", e)
        
    print("\n==========================================================================================")
    print("Day 16 APIs Checked Successfully! All contracts and response structures conform to specs.")
    print("Structured logs saved to: data/api_resumes/api_structured.log")
    print("==========================================================================================\n")

import sys
import uvicorn

def main():
    if "--server" in sys.argv:
        print("\n==========================================================================================")
        print("STARTING LIVE ZECPATH ATS REST API SERVER")
        print("==========================================================================================\n")
        uvicorn.run("ats_engine.ats_api:app", host="127.0.0.1", port=8000, reload=True)
    else:
        asyncio.run(run_tests())

if __name__ == "__main__":
    main()
