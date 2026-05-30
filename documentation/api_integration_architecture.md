# Zecpath AI Integration Architecture

## Integration Overview
```
Candidate/Recruiter Dashboard
             ↓
Backend Application Gateway
             ↓
-----------------------------------------------------------------
API Orchestration Gateway (JWT token verification)
-----------------------------------------------------------------
  * Resume API      → POST /resume/upload   (Async Queue)
  * ATS API         → POST /ats/score       (Sync evaluation)
  * Screening API   → POST /screening/run   (Sync dialogue loops)
  * Interview AI    → POST /interview/run   (Sync behavior rating)
  * Decision Engine → POST /decision/final  (Sync recommendation)
-----------------------------------------------------------------
             ↓
Database Profiler (MySQL/PostgreSQL) ↔ File Storage (Transcripts/Reports)
```

---

## Request & Response JSON Contract Schemas

### 1. Resume Parsing API
* **Endpoint**: `/resume/parse` (Async)
* **Request Payload**:
  ```json
  {
    "candidate_id": "C100",
    "file_url": "https://s3.amazonaws.com/resumes/c100.pdf"
  }
  ```
* **Response Payload**:
  ```json
  {
    "candidate_id": "C100",
    "parsed_data": {
      "skills": ["Python", "Django", "PostgreSQL"],
      "experience_years": 2.5
    }
  }
  ```

---

### 2. ATS Scoring API
* **Endpoint**: `/ats/score` (Sync)
* **Request Payload**:
  ```json
  {
    "candidate_profile": {
      "skills": ["Python", "Django"],
      "experience_years": 2.5
    },
    "job_description": {
      "required_skills": ["Python", "Flask"],
      "minimum_experience": 2
    }
  }
  ```
* **Response Payload**:
  ```json
  {
    "ats_score": 78,
    "match_details": {
      "matched_skills": ["Python"],
      "missing_skills": ["Flask"]
    }
  }
  ```

---

### 3. Final Recommendation Decision API
* **Endpoint**: `/decision/final` (Sync)
* **Request Payload**:
  ```json
  {
    "scores": {
      "ats": 78,
      "screening": 72,
      "hr": 80,
      "technical": 85,
      "machine_test": 76
    },
    "risk_flags": {
      "behavior": "Low Risk",
      "integrity": "Moderate Risk"
    }
  }
  ```
* **Response Payload**:
  ```json
  {
    "decision": "Hold / Review",
    "adjusted_score": 73,
    "confidence": 88
  }
  ```

---

## Sync vs Async Ingestion Designs

* **Async processing**: Used for resource-heavy operations like document parsing and report generation. The requests are pushed to a Redis queue, and the client polls or waits for a webhook call.
* **Sync processing**: Used for low-latency dialogue responses and scoring evaluations. Requires prompt inference to prevent client-side wait hangs.
