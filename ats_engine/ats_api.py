# ats_engine/ats_api.py - FastAPI REST APIs and Schema Integration for Zecpath AI.

import os
import json
import uuid
import datetime
import re
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

# Ensure directories
UPLOAD_DIR = "data/api_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)
REGISTRY_FILE = "data/api_resumes/registry.json"
JOBS_FILE = "data/api_resumes/jobs.json"

# Structured Logger
def log_structured(level: str, message: str, candidate_id: Optional[str] = None, job_id: Optional[str] = None):
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "service": "ATS Engine",
        "level": level,
        "message": message
    }
    if candidate_id:
        log_entry["candidate_id"] = candidate_id
    if job_id:
        log_entry["job_id"] = job_id
        
    # Print to console (standard logging stdout)
    print(json.dumps(log_entry))
    
    # Save log entry
    try:
        log_file = "data/api_resumes/api_structured.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except:
        pass

# Registry helpers
def load_json_store(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_json_store(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Custom Exceptions
class ATSAPIException(Exception):
    def __init__(self, error_code: str, message: str, status_code: int = 400):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.timestamp = datetime.datetime.utcnow().isoformat() + "Z"

app = FastAPI(title="Zecpath ATS AI API", version="1.0.0")

@app.on_event("startup")
def open_browser_automatically():
    import webbrowser
    import threading
    import time
    def open_swagger():
        time.sleep(1.5) # Wait for Uvicorn server to bind and start
        try:
            webbrowser.open("http://127.0.0.1:8000/docs")
        except:
            pass
    threading.Thread(target=open_swagger, daemon=True).start()

@app.exception_handler(ATSAPIException)
async def ats_exception_handler(request, exc: ATSAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error_code": exc.error_code,
            "message": exc.message,
            "timestamp": exc.timestamp
        }
    )

# -------------------------------
# Input / Output Pydantic Schemas
# -------------------------------
class ParseRequest(BaseModel):
    resume_id: str

class ScoreRequest(BaseModel):
    candidate_id: str
    job_id: str

class ShortlistRequest(BaseModel):
    job_id: str

class StartJobRequest(BaseModel):
    resume_id: str
    job_id: str

# -------------------------------
# API Endpoints
# -------------------------------

@app.get("/")
def home():
    return {"message": "Zecpath ATS API Running"}

@app.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_id: str = Form(...),
    candidate_id: str = Form(...)
):
    log_structured("INFO", "Initiated resume upload", candidate_id=candidate_id, job_id=job_id)
    
    # Validation
    if not job_id.strip():
        log_structured("WARNING", "Upload failed: Missing job_id", candidate_id=candidate_id)
        raise ATSAPIException("INVALID_INPUT", "Missing job_id", 400)
    if not candidate_id.strip():
        log_structured("WARNING", "Upload failed: Missing candidate_id", job_id=job_id)
        raise ATSAPIException("INVALID_INPUT", "Missing candidate_id", 400)
        
    filename = file.filename
    ext = filename.split(".")[-1].lower() if "." in filename else "txt"
    if ext not in ["txt", "pdf", "docx", "doc"]:
        log_structured("ERROR", f"Upload failed: Invalid format {ext}", candidate_id=candidate_id, job_id=job_id)
        raise ATSAPIException("INVALID_INPUT", "Unsupported file type", 400)
        
    # Create unique IDs
    resume_id = "R" + str(uuid.uuid4().int)[:6]
    
    # Save raw file
    raw_path = os.path.join(UPLOAD_DIR, f"{resume_id}.{ext}")
    try:
        content = await file.read()
        with open(raw_path, "wb") as f:
            f.write(content)
            
        # Standardize content to clean text immediately
        text_content = ""
        if ext == "txt":
            text_content = content.decode("utf-8", errors="ignore")
        else:
            # Fallback to importing text extractors if possible
            try:
                from parsers.resume_extractor import extract_resume
                parsed_res = extract_resume(raw_path)
                if isinstance(parsed_res, dict):
                    text_content = parsed_res.get("cleaned_text", "")
                else:
                    text_content = str(parsed_res)
            except:
                text_content = content.decode("utf-8", errors="ignore")
                
        # Save clean text
        clean_path = os.path.join(UPLOAD_DIR, f"{resume_id}_cleaned.txt")
        with open(clean_path, "w", encoding="utf-8") as f:
            f.write(text_content)
            
        # Update registry
        registry = load_json_store(REGISTRY_FILE)
        registry[resume_id] = {
            "resume_id": resume_id,
            "candidate_id": candidate_id,
            "job_id": job_id,
            "filename": filename,
            "raw_path": raw_path,
            "clean_path": clean_path,
            "uploaded_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        save_json_store(REGISTRY_FILE, registry)
        
        log_structured("INFO", "Resume uploaded successfully", candidate_id=candidate_id, job_id=job_id)
        return {
            "status": "success",
            "message": "Resume uploaded successfully",
            "resume_id": resume_id,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        log_structured("ERROR", f"File save failure: {str(e)}", candidate_id=candidate_id, job_id=job_id)
        raise ATSAPIException("SERVER_ERROR", f"Internal storage failure: {str(e)}", 500)

@app.post("/resume/parse")
def parse_resume(req: ParseRequest):
    resume_id = req.resume_id
    log_structured("INFO", f"Parsing request for resume {resume_id}")
    
    registry = load_json_store(REGISTRY_FILE)
    if resume_id not in registry:
        log_structured("WARNING", f"Parse failed: Resume {resume_id} not found")
        raise ATSAPIException("NOT_FOUND", "Resume not found", 404)
        
    candidate_info = registry[resume_id]
    candidate_id = candidate_info["candidate_id"]
    clean_path = candidate_info["clean_path"]
    
    try:
        with open(clean_path, "r", encoding="utf-8") as f:
            text = f.read()
            
        # Core Parser imports
        from parsers.education_parser import extract_education
        from ats_engine.skill_extractor import extract_skills_with_confidence
        from ats_engine.experience_parser import extract_experience_blocks, extract_roles
        from parsers.section_classifier import detect_sections
        
        sections = detect_sections(text)
        skills_data = extract_skills_with_confidence(text)
        skills = [item["skill"] for item in skills_data if item.get("skill")]
        
        exp_text = "\n".join(sections.get("experience", []))
        experiences = extract_experience_blocks(exp_text)
        roles = extract_roles(text)
        education = extract_education(text)
        
        # Save parsed profile in registry
        candidate_info["parsed_profile"] = {
            "skills": skills,
            "experience": experiences,
            "education": education,
            "roles": roles
        }
        registry[resume_id] = candidate_info
        save_json_store(REGISTRY_FILE, registry)
        
        log_structured("INFO", "Parsing completed successfully", candidate_id=candidate_id)
        return {
            "candidate_id": candidate_id,
            "parsed_profile": {
                "skills": skills,
                "experience": experiences,
                "education": education
            },
            "status": "completed"
        }
    except Exception as e:
        log_structured("ERROR", f"Parsing failure: {str(e)}", candidate_id=candidate_id)
        raise ATSAPIException("PROCESSING_ERR", f"Resume parsing failed: {str(e)}", 500)

@app.post("/ats/score")
def score_candidate(req: ScoreRequest):
    candidate_id = req.candidate_id
    job_id = req.job_id
    log_structured("INFO", "Candidate scoring requested", candidate_id=candidate_id, job_id=job_id)
    
    registry = load_json_store(REGISTRY_FILE)
    
    # Locate candidate by candidate_id in registry
    candidate_info = None
    for r_id, info in registry.items():
        if info.get("candidate_id") == candidate_id:
            candidate_info = info
            break
            
    if not candidate_info:
        log_structured("WARNING", "Scoring failed: Candidate not found", candidate_id=candidate_id)
        raise ATSAPIException("NOT_FOUND", "Candidate profile not found", 404)
        
    parsed = candidate_info.get("parsed_profile")
    if not parsed:
        log_structured("WARNING", "Scoring failed: Candidate profile unparsed", candidate_id=candidate_id)
        raise ATSAPIException("INVALID_INPUT", "Candidate profile not parsed yet", 400)
        
    # Load JDs
    jds_dir = "data/processed_jds"
    jd_files = [f for f in os.listdir(jds_dir) if f.endswith(".json")]
    jd_profiles = []
    for f in jd_files:
        with open(os.path.join(jds_dir, f), "r", encoding="utf-8") as file:
            jd_profiles.append(json.load(file))
            
    # Reference/Default Job
    matched_jd = None
    for jd in jd_profiles:
        if jd.get("job_id") == job_id or jd.get("job_title", "").lower().strip() == job_id.lower().strip():
            matched_jd = jd
            break
            
    if not matched_jd:
        # Fallback to reference JD
        for jd in jd_profiles:
            if "tool" in jd.get("job_title", "").lower() and "die" in jd.get("job_title", "").lower():
                matched_jd = jd
                break
        if not matched_jd and jd_profiles:
            matched_jd = jd_profiles[0]
            
    if not matched_jd:
        log_structured("ERROR", "Scoring failed: No JDs found in database", candidate_id=candidate_id, job_id=job_id)
        raise ATSAPIException("NOT_FOUND", "No job descriptions available", 404)
        
    try:
        # Compute scores
        # 1. Skill Score
        candidate_skills = parsed.get("skills", [])
        jd_skills = matched_jd.get("required_skills", [])
        matched = set(s.lower().replace("_", " ") for s in candidate_skills).intersection(
            set(s.lower().replace("_", " ") for s in jd_skills)
        )
        skill_score = round((len(matched) / len(jd_skills)) * 100.0, 2) if jd_skills else 0.0
        
        # 2. Experience Score
        from ats_engine.experience_parser import calculate_relevance
        roles = parsed.get("roles", [])
        exp_score = calculate_relevance(roles, matched_jd.get("job_title"))
        
        # 3. Education Score
        from parsers.education_parser import calculate_education_relevance, DEGREE_MAP
        education_list = parsed.get("education", [])
        candidate_degree = education_list[0]["degree"] if education_list else "None"
        req_degree = matched_jd.get("education_required", "")
        req_degree_normalized = "B.Tech"
        for deg in ["diploma", "iti", "b.tech", "b.e", "m.tech", "mba", "bsc", "msc"]:
            if deg in req_degree.lower():
                req_degree_normalized = DEGREE_MAP.get(deg.replace(".", ""), deg.title())
                break
        education_relevance = calculate_education_relevance(candidate_degree, req_degree_normalized) * 100.0
        
        # 4. Semantic Score
        from ats_engine.semantic_matcher import match_resume_to_jd
        resume_obj = {
            "skills": candidate_skills,
            "experience": parsed.get("experience", []),
            "projects": []  # Empty fallback
        }
        semantic_results = match_resume_to_jd(resume_obj, matched_jd)
        semantic_score = semantic_results["final_similarity_score"]
        
        # Dynamic Weights logic
        from ats_engine.ats_scorer import generate_candidate_score
        cand_score_input = {
            "candidate_id": candidate_id,
            "skill_score": skill_score,
            "experience_score": exp_score,
            "education_score": education_relevance,
            "semantic_score": semantic_score
        }
        score_data = generate_candidate_score(cand_score_input, matched_jd)
        
        log_structured("INFO", "Candidate scoring completed", candidate_id=candidate_id, job_id=job_id)
        return {
            "candidate_id": candidate_id,
            "final_score": score_data["final_score"],
            "breakdown": {
                "skills": round(skill_score),
                "experience": round(exp_score),
                "education": round(education_relevance),
                "semantic": round(semantic_score)
            }
        }
    except Exception as e:
        log_structured("ERROR", f"Scoring engine exception: {str(e)}", candidate_id=candidate_id, job_id=job_id)
        raise ATSAPIException("PROCESSING_ERR", f"ATS scoring failed: {str(e)}", 500)

@app.post("/ats/shortlist")
def shortlist_candidates(req: ShortlistRequest):
    job_id = req.job_id
    log_structured("INFO", "Shortlist generation requested", job_id=job_id)
    
    registry = load_json_store(REGISTRY_FILE)
    
    candidates_pool = []
    
    # Process all profiles matching job_id
    for r_id, info in registry.items():
        if info.get("job_id") == job_id and "parsed_profile" in info:
            cand_id = info["candidate_id"]
            # Call local scoring to build score dictionary
            try:
                score_response = score_candidate(ScoreRequest(candidate_id=cand_id, job_id=job_id))
                candidates_pool.append({
                    "candidate_id": cand_id,
                    "final_score": score_response["final_score"],
                    "skill_score": score_response["breakdown"]["skills"],
                    "experience_score": score_response["breakdown"]["experience"],
                    "education_score": score_response["breakdown"]["education"],
                    "semantic_score": score_response["breakdown"]["semantic"]
                })
            except:
                pass
                
    if not candidates_pool:
        log_structured("WARNING", "Shortlist generation failed: No candidates evaluated", job_id=job_id)
        raise ATSAPIException("NOT_FOUND", "No candidate scores found for this job ID", 404)
        
    try:
        from ats_engine.ranking_engine import ranking_pipeline
        pipeline_results = ranking_pipeline(candidates_pool)
        ranked_list = pipeline_results["ranked_list"]
        
        response_candidates = []
        for c in ranked_list:
            response_candidates.append({
                "candidate_id": c["candidate_id"],
                "score": round(c["final_score"]),
                "status": c["status"]
            })
            
        shortlisted_count = sum(1 for c in response_candidates if c["status"] == "Shortlisted")
        
        log_structured("INFO", "Shortlist generated successfully", job_id=job_id)
        return {
            "job_id": job_id,
            "total_candidates": len(response_candidates),
            "shortlisted": shortlisted_count,
            "candidates": response_candidates
        }
    except Exception as e:
        log_structured("ERROR", f"Ranking pipeline failure: {str(e)}", job_id=job_id)
        raise ATSAPIException("PROCESSING_ERR", f"Shortlisting failed: {str(e)}", 500)

# -------------------------------
# Async Job Handling endpoints
# -------------------------------

@app.post("/jobs/start")
def start_job(req: StartJobRequest):
    resume_id = req.resume_id
    job_id = req.job_id
    log_structured("INFO", f"Job start requested for resume {resume_id}", job_id=job_id)
    
    registry = load_json_store(REGISTRY_FILE)
    if resume_id not in registry:
        raise ATSAPIException("NOT_FOUND", "Resume not found", 404)
        
    job_uid = "JOB" + str(uuid.uuid4().int)[:6]
    
    # Save job status
    jobs = load_json_store(JOBS_FILE)
    jobs[job_uid] = {
        "job_id": job_uid,
        "resume_id": resume_id,
        "candidate_id": registry[resume_id]["candidate_id"],
        "job_code": job_id,
        "status": "processing",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    save_json_store(JOBS_FILE, jobs)
    
    log_structured("INFO", f"Job {job_uid} queued", job_id=job_id)
    return {
        "job_id": job_uid,
        "status": "processing"
    }

@app.get("/jobs/status/{job_uid}")
def check_job_status(job_uid: str):
    log_structured("INFO", f"Job status check requested for {job_uid}")
    
    jobs = load_json_store(JOBS_FILE)
    if job_uid not in jobs:
        raise ATSAPIException("NOT_FOUND", "Job status record not found", 404)
        
    job_info = jobs[job_uid]
    
    # Process job if still "processing"
    if job_info["status"] == "processing":
        try:
            # Synchronously run parse and score to simulate worker processing
            resume_id = job_info["resume_id"]
            parse_resume(ParseRequest(resume_id=resume_id))
            score_candidate(ScoreRequest(candidate_id=job_info["candidate_id"], job_id=job_info["job_code"]))
            
            job_info["status"] = "completed"
            job_info["result_url"] = f"/ats/result/{job_info['candidate_id']}"
            jobs[job_uid] = job_info
            save_json_store(JOBS_FILE, jobs)
            log_structured("INFO", f"Job {job_uid} processing finished", candidate_id=job_info["candidate_id"])
        except Exception as e:
            job_info["status"] = "failed"
            job_info["error"] = str(e)
            jobs[job_uid] = job_info
            save_json_store(JOBS_FILE, jobs)
            log_structured("ERROR", f"Job {job_uid} processing failed: {str(e)}", candidate_id=job_info["candidate_id"])
            
    return {
        "job_id": job_uid,
        "status": job_info["status"],
        "result_url": job_info.get("result_url")
    }
