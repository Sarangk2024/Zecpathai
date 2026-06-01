# Zecpath AI System – Complete Technical Handbook

## 1. System Overview
Zecpath AI is a comprehensive intelligent hiring platform designed to automate the recruitment funnel. It extracts resume content, filters candidates using ATS scoring, facilitates automated screening and HR interviews, evaluates technical skill depth, assesses coding correctness, logs behavioral risks, and generates recruiter summaries.

---

## 2. Full System Architecture
```
        Candidate / Recruiter Dashboard (Frontend Interface)
                           ↓
              Backend API Orchestration Gateway
                           ↓
-----------------------------------------------------------
                AI Microservices Layer
-----------------------------------------------------------
  * Resume Parser  → POST /resume/parse
  * ATS Scorer     → POST /ats/score
  * Screening AI   → POST /screening/run
  * HR Round AI    → POST /interview/run
  * Technical AI   → POST /technical/run
  * Sandbox AI     → POST /machine/evaluate
  * Decisions AI   → POST /decision/final
-----------------------------------------------------------
                           ↓
       Database Registry  ↔  Observability & Log Audits
```

---

## 3. End-to-End Workflow
```
Candidate Resume Submissions
          ↓
   ATS Match Filter
          ↓
Outbound Screening Call (Intent Checks)
          ↓
 HR Round Behavioral Analytics
          ↓
Technical Coding Sandbox Evaluation
          ↓
Cheating Prevention telemetry validation
          ↓
Aggregation & Final Decision logic
          ↓
Recruiter PDF Report Export
```

---

## 4. API Endpoints Specifications

### POST `/resume/parse`
Extracts structured information from `.pdf` and `.docx` candidate profiles.

### POST `/ats/score`
Cross-references extracted candidate details against Job Descriptions.

### POST `/decision/final`
Integrates score parameters and applies risk penalties to formulate the selection status.

---

## 5. Scoring Logic Formulas
$$\text{Final Score} = (\text{ATS} \times 0.20) + (\text{Screening} \times 0.15) + (\text{HR} \times 0.20) + (\text{Technical} \times 0.25) + (\text{Machine Test} \times 0.20)$$

* **Risk Penalties**: Deducts `-10` for Moderate/High Behavior Risk and `-15` for Cheating/Integrity violations.
* **Consistency Scoring**: Variance $<10 \implies +5$ bonus; Variance $>30 \implies -5$ penalty.

---

## 6. Setup & Deployment Guide

### local Installation
1. Clone the codebase repository:
   ```bash
   git clone https://github.com/Sarangk2024/Zecpathai.git
   ```
2. Initialize virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run python pipelines:
   ```bash
   python run_d63_demo_dataset.py
   ```

### Production Deployment
* Containerize services using Docker.
* Orchestrate scaling clusters via Kubernetes (EKS/GKE).
* Set up Nginx/Cloudflare reverse proxy load balancers.
* Integrate Prometheus + Grafana dashboards tracking logging metrics.
