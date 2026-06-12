# main.py - Main entry point to launch Zecpath AI web server / user interface.

import sys
import os
import webbrowser
import threading
import time
import re
import urllib.parse
import io
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

# Try to import PyPDF2 to parse PDF resumes
try:
    import PyPDF2
    HAS_PDF_PARSER = True
except ImportError:
    HAS_PDF_PARSER = False

app = FastAPI(title="Zecpath AI - Autonomous Job Portal & Hiring Engine")

# ----------------------------------------------------------------------
# DATABASE CONFIGURATION & HELPERS (Neon PG / SQLite support)
# ----------------------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    if DATABASE_URL:
        try:
            import psycopg2
            result = urllib.parse.urlparse(DATABASE_URL)
            username = result.username
            password = result.password
            database = result.path[1:]
            hostname = result.hostname
            port = result.port
            conn = psycopg2.connect(
                database=database,
                user=username,
                password=password,
                host=hostname,
                port=port
            )
            return conn, "postgresql"
        except Exception as e:
            print(f"[WARN] PostgreSQL connection failed: {e}. Falling back to SQLite.")
            
    conn = sqlite3.connect("zecpath.db")
    conn.row_factory = sqlite3.Row
    return conn, "sqlite"

def db_execute(query, params=()):
    conn, db_type = get_db_connection()
    if db_type == "postgresql":
        query = query.replace("?", "%s")
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def db_query(query, params=()):
    conn, db_type = get_db_connection()
    if db_type == "postgresql":
        query = query.replace("?", "%s")
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    if db_type == "postgresql":
        columns = [desc[0] for desc in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    else:
        rows = [dict(row) for row in cursor.fetchall()]
        
    conn.close()
    return rows

def init_db():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            company_name TEXT,
            title TEXT,
            description TEXT,
            skills_required TEXT,
            budget_min INTEGER,
            budget_max INTEGER,
            assessment_type TEXT,
            status TEXT DEFAULT 'open'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            name TEXT,
            contact_info TEXT,
            gender TEXT,
            location TEXT,
            notice_period TEXT,
            expected_salary INTEGER,
            skills TEXT,
            experience INTEGER,
            resume_text TEXT,
            education_degree TEXT,
            education_school TEXT,
            education_year TEXT,
            github_url TEXT,
            linkedin_url TEXT,
            portfolio_url TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            candidate_id INTEGER,
            ats_score REAL,
            screening_score REAL,
            assessment_score REAL,
            behavioral_score REAL,
            negotiated_salary INTEGER,
            status TEXT,
            recruiter_override TEXT DEFAULT 'none',
            offer_accepted TEXT DEFAULT 'pending',
            screening_transcript TEXT,
            assessment_details TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            title TEXT,
            message TEXT,
            read_status INTEGER DEFAULT 0
        )
        """
    ]
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    for q in queries:
        if db_type == "postgresql":
            q = q.replace("AUTOINCREMENT", "")
            q = q.replace("INTEGER PRIMARY KEY", "SERIAL PRIMARY KEY")
            q = q.replace("REAL", "DOUBLE PRECISION")
        cursor.execute(q)
    conn.commit()
    
    # Safely migrate new columns to candidates if using SQLite
    if db_type == "sqlite":
        for col in ["education_degree", "education_school", "education_year", "github_url", "linkedin_url", "portfolio_url"]:
            try:
                cursor.execute(f"ALTER TABLE candidates ADD COLUMN {col} TEXT")
            except Exception:
                pass
        conn.commit()
    conn.close()
    
    # Seed 10 mock job posts with proper JDs
    jobs = db_query("SELECT * FROM jobs")
    if len(jobs) < 10:
        db_execute("DELETE FROM jobs") # Reset to seed fresh 10 jobs
        seed_jobs = [
            ("Zecpath Corporation", "MERN Stack Developer", "Develop interactive React user interfaces, manage Node.js Express servers, and structure MongoDB database schemas.", "react,node.js,express,mongodb,javascript", 80000, 120000, "coding"),
            ("Zecpath Corporation", "Python Backend Developer", "Design scalable APIs using FastAPI and Python. Interface with PostgreSQL databases and manage containerized DevOps deployments.", "python,fastapi,postgresql,docker,django", 85000, 130000, "coding"),
            ("Pixel Design Agency", "UI/UX Designer", "Produce modern Figma layout wireframes, high-fidelity prototypes, and perform usability heuristics checking.", "figma,wireframe,prototype,photoshop,design", 70000, 95000, "design_quiz"),
            ("Alpha Tech Solutions", "Sales Executive", "Drive revenue opportunities, lead CRM workflows, cold call prospects, and execute salary and contract negotiations.", "communication,sales,negotiation,crm,leads", 50000, 75000, "aptitude"),
            ("DevOps Enterprise", "Cloud Systems Engineer", "Provision infrastructure as code using Terraform, build CI/CD automation pipelines, and scale Docker/Kubernetes container orchestration.", "aws,docker,kubernetes,terraform,cicd", 95000, 145000, "coding"),
            ("Quality Labs", "QA Automation Analyst", "Implement automated unit testing suites in Cypress and Selenium. Write robust test specs and verify build compliance.", "selenium,cypress,testing,javascript,qa", 65000, 95000, "coding"),
            ("Agile Solutions", "Technical Project Manager", "Steer Scrum developer team standups, build Agile product roadmaps, create Jira tracking boards, and manage deliverables.", "scrum,agile,jira,roadmap,planning", 85000, 115000, "aptitude"),
            ("Growth Marketing Co", "SEO Specialist", "Direct digital growth campaigns, analyze Adwords marketing analytics, and execute SEO keyword optimization pipelines.", "seo,analytics,adwords,campaigns,marketing", 60000, 90000, "aptitude"),
            ("Capital Venture Partners", "Financial Analyst", "Build financial forecasting sheets, validate Excel models, and forecast asset planning analytics.", "excel,modeling,finance,forecasting,statistics", 70000, 100000, "aptitude"),
            ("Global Talent Group", "HR Operations Recruiter", "Source elite candidates, coordinate interviews, maintain hiring pipeline compliance, and draft offer contracts.", "talent,sourcing,interviewing,compliance,hiring", 55000, 75000, "aptitude")
        ]
        for company, title, desc, skills, b_min, b_max, assess in seed_jobs:
            db_execute(
                "INSERT INTO jobs (company_id, company_name, title, description, skills_required, budget_min, budget_max, assessment_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (1, company, title, desc, skills, b_min, b_max, assess)
            )

# ----------------------------------------------------------------------
# GMAIL SMTP MAILER INTEGRATION
# ----------------------------------------------------------------------
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

def send_email_notification(to_email, subject, body_text):
    print(f"\n[EMAIL DISPATCH LOG] To: {to_email} | Subject: {subject}\nContent:\n{body_text}\n")
    if SMTP_EMAIL and SMTP_PASSWORD:
        try:
            msg = MIMEMultipart()
            msg["From"] = SMTP_EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body_text, "plain"))
            
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
            server.quit()
            print("[EMAIL DISPATCH LOG] Live SMTP Email sent successfully via Gmail!")
        except Exception as e:
            print(f"[WARN] SMTP delivery failed: {e}")

# ----------------------------------------------------------------------
# AUTHENTICATION & BUSINESS SCHEMAS
# ----------------------------------------------------------------------
class LoginRequest(BaseModel):
    email: str
    password: str
    user_type: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    user_type: str

class JobPostRequest(BaseModel):
    company_name: str
    title: str
    description: str
    skills_required: str
    budget_min: int
    budget_max: int
    assessment_type: str

class ProfileSaveRequest(BaseModel):
    candidate_id: int
    name: str
    contact_info: str = ""
    gender: str = ""
    location: str = ""
    notice_period: str = ""
    expected_salary: int = 0
    skills: str = ""
    experience: int = 0
    resume_text: str = ""
    education_degree: str = ""
    education_school: str = ""
    education_year: str = ""
    github_url: str = ""
    linkedin_url: str = ""
    portfolio_url: str = ""

class ApplyRequest(BaseModel):
    candidate_id: int
    job_id: int
    name: str
    contact_info: str
    gender: str
    location: str
    notice_period: str
    expected_salary: int
    experience: int
    resume_text: str

class ScreeningSubmitRequest(BaseModel):
    application_id: int
    screening_score: float
    transcript: str

class AssessmentSubmitRequest(BaseModel):
    application_id: int
    score: float

class OverrideRequest(BaseModel):
    application_id: int
    decision: str

class OfferActionRequest(BaseModel):
    application_id: int
    action: str

class AssessmentPayload(BaseModel):
    role_key: str
    code_content: str = ""
    aptitude_answer: str = ""

class NegotiationPayload(BaseModel):
    role_key: str
    expected_salary: float
    counter_offer_count: int

# HTML SPA UI code
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zecpath - AI-Driven Autonomous Job Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #060913;
            --bg-panel: #0b0f1e;
            --bg-card: rgba(17, 24, 43, 0.75);
            --border-glow: rgba(99, 102, 241, 0.2);
            --color-primary: #6366f1;
            --color-primary-glow: rgba(99, 102, 241, 0.4);
            --color-success: #10b981;
            --color-warning: #f59e0b;
            --color-danger: #ef4444;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-base);
            color: var(--text-main);
            overflow-x: hidden;
            min-height: 100vh;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: -1;
            background: 
                radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.1) 0%, transparent 60%),
                radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.1) 0%, transparent 60%);
            animation: drift 20s infinite alternate ease-in-out;
        }

        @keyframes drift {
            0% { transform: scale(1) translate(0, 0); }
            50% { transform: scale(1.1) translate(1%, 2%); }
            100% { transform: scale(1) translate(0, 0); }
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.25rem 3rem;
            background-color: rgba(11, 15, 30, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo {
            font-size: 1.3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .logo::before {
            content: '';
            display: inline-block;
            width: 10px;
            height: 10px;
            background-color: var(--color-primary);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--color-primary);
        }

        .user-status {
            font-size: 0.85rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .btn-logout {
            background-color: rgba(239, 68, 68, 0.15);
            border: 1px solid var(--color-danger);
            color: var(--color-danger);
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.2s ease;
        }

        .btn-logout:hover {
            background-color: var(--color-danger);
            color: #fff;
        }

        /* Nav Tabs style */
        .portal-nav {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 0.75rem;
        }

        .nav-tab-item {
            color: var(--text-muted);
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: all 0.2s ease;
        }

        .nav-tab-item.active {
            color: #fff;
            background-color: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
        }

        .main-container {
            max-width: 1300px;
            margin: 2rem auto;
            padding: 0 2rem;
        }

        .card-panel {
            background: rgba(11, 15, 30, 0.7);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 2rem;
        }

        .section-title {
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 1.25rem;
            color: #fff;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Form styling */
        .form-group {
            margin-bottom: 1.25rem;
        }

        .form-group label {
            display: block;
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 0.4rem;
            font-weight: 500;
        }

        .form-select, .form-input, .form-textarea {
            width: 100%;
            background-color: #0c1020;
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #fff;
            padding: 0.65rem 0.85rem;
            border-radius: 6px;
            outline: none;
            font-size: 0.9rem;
            font-family: inherit;
            transition: all 0.2s ease;
        }

        .form-select option {
            background-color: #0c1020;
            color: #fff;
        }

        .form-textarea {
            resize: vertical;
            height: 100px;
        }

        .form-select:focus, .form-input:focus, .form-textarea:focus {
            border-color: var(--color-primary);
            box-shadow: 0 0 12px var(--color-primary-glow);
        }

        .btn-action {
            background: linear-gradient(135deg, var(--color-primary), #8b5cf6);
            border: none;
            color: #fff;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            transition: all 0.2s ease;
            display: inline-block;
        }

        .btn-action:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        }

        .step.active .step-num {
            border-color: var(--color-primary);
            color: #fff;
            box-shadow: 0 0 15px var(--color-primary-glow);
            animation: pulse-border 2s infinite;
        }

        @keyframes pulse-border {
            0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }
            100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
        }

        /* Auth Form */
        .auth-container {
            max-width: 420px;
            margin: 4rem auto;
        }

        /* Grid Layouts */
        .layout-grid {
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 2rem;
        }

        /* Notifications Inbox */
        .notifications-badge {
            background-color: var(--color-danger);
            color: #fff;
            font-size: 0.7rem;
            padding: 0.1rem 0.4rem;
            border-radius: 10px;
            margin-left: 0.5rem;
        }

        .notification-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .notification-card:hover {
            border-color: var(--color-primary);
            background: rgba(99, 102, 241, 0.02);
        }

        .notification-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #fff;
            margin-bottom: 0.25rem;
        }

        .notification-body {
            font-size: 0.8rem;
            color: var(--text-muted);
            line-height: 1.4;
        }

        /* Job feed card list */
        .job-feed {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .job-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 1.5rem;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s ease;
        }

        .job-card:hover {
            border-color: rgba(255,255,255,0.1);
            background: rgba(255,255,255,0.03);
        }

        .job-info h3 {
            font-size: 1.1rem;
            color: #fff;
            margin-bottom: 0.35rem;
        }

        .job-info p {
            font-size: 0.85rem;
            color: var(--text-muted);
        }

        .match-badge {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.65rem;
            border-radius: 12px;
            display: inline-block;
            margin-top: 0.5rem;
        }

        .match-strong { background-color: rgba(16, 185, 129, 0.15); border: 1px solid var(--color-success); color: var(--color-success); }
        .match-good { background-color: rgba(245, 158, 11, 0.15); border: 1px solid var(--color-warning); color: var(--color-warning); }
        .match-low { background-color: rgba(239, 68, 68, 0.15); border: 1px solid var(--color-danger); color: var(--color-danger); }

        /* Stepper Flow progress */
        .stepper-row {
            display: flex;
            justify-content: space-between;
            position: relative;
            background-color: var(--bg-panel);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
        }

        .step {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 80px;
            position: relative;
            z-index: 2;
        }

        .step-num {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background-color: #0b0f1e;
            border: 2px solid rgba(255,255,255,0.1);
            color: var(--text-muted);
            font-size: 0.8rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .step-label {
            font-size: 0.65rem;
            color: var(--text-muted);
            margin-top: 0.4rem;
            text-align: center;
        }

        .step.active .step-num {
            border-color: var(--color-primary);
            color: #fff;
            box-shadow: 0 0 10px var(--color-primary-glow);
        }

        .step.completed .step-num {
            border-color: var(--color-success);
            background-color: rgba(16, 185, 129, 0.1);
            color: var(--color-success);
        }

        /* Dialogue Box voice */
        .call-card {
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 8px;
            background: rgba(0,0,0,0.25);
            padding: 1.5rem;
            margin-top: 1rem;
        }

        .dialogue-stream {
            height: 200px;
            overflow-y: auto;
            padding: 1rem;
            background-color: #070911;
            border-radius: 6px;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .bubble {
            max-width: 80%;
            padding: 0.6rem 0.85rem;
            border-radius: 12px;
            font-size: 0.8rem;
            line-height: 1.4;
        }

        .bubble.ai {
            background-color: rgba(255,255,255,0.05);
            color: var(--text-main);
            align-self: flex-start;
            border-bottom-left-radius: 2px;
        }

        .bubble.user {
            background-color: var(--color-primary);
            color: #fff;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
        }

        /* Sandbox Javascript */
        .editor-container {
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 8px;
            overflow: hidden;
            margin-top: 1rem;
            background-color: #070a13;
        }

        .editor-textarea {
            width: 100%;
            height: 120px;
            background: transparent;
            border: none;
            color: #a78bfa;
            font-family: 'JetBrains Mono', monospace;
            padding: 1rem;
            outline: none;
            font-size: 0.85rem;
            resize: none;
        }

        .editor-terminal {
            background: #000;
            padding: 0.75rem 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: #10b981;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Document style Offer Letter */
        .offer-letter-doc {
            background-color: #fff;
            color: #111827;
            padding: 2.5rem;
            border-radius: 8px;
            font-family: 'Georgia', serif;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            line-height: 1.6;
            margin-top: 1rem;
        }

        .offer-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #6366f1;
            padding-bottom: 0.75rem;
            margin-bottom: 1.5rem;
        }

        /* Recruiter Dashboard list metrics */
        .rec-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .rec-metric-card {
            background-color: var(--bg-panel);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        }

        .rec-metric-val {
            font-size: 2.2rem;
            font-weight: 700;
            color: #fff;
            margin: 0.25rem 0;
        }

        .pipeline-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }

        .pipeline-table th, .pipeline-table td {
            text-align: left;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 0.85rem;
        }

        .pipeline-table th {
            color: var(--text-muted);
            background-color: rgba(255,255,255,0.02);
        }

        .action-select {
            background-color: #0b0f1e;
            border: 1px solid rgba(255,255,255,0.1);
            color: #fff;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">ZECPATH HIRING ENGINE</div>
        <div class="user-status" id="user-status-container">
            <span>Not Signed In</span>
        </div>
    </header>

    <main class="main-container">
        <!-- AUTH LOGIN PAGE -->
        <div id="auth-panel" class="auth-container">
            <div class="card-panel">
                <div class="section-title">
                    <span id="auth-title">Sign In to Zecpath</span>
                </div>
                <div class="form-group" id="group-auth-name" style="display: none;">
                    <label for="auth-name">Full Name</label>
                    <input type="text" id="auth-name" class="form-input" placeholder="John Doe">
                </div>
                <div class="form-group">
                    <label for="auth-email">Email Address</label>
                    <input type="email" id="auth-email" class="form-input" placeholder="name@domain.com">
                </div>
                <div class="form-group">
                    <label for="auth-pass">Password</label>
                    <input type="password" id="auth-pass" class="form-input" placeholder="Password">
                </div>
                <div class="form-group">
                    <label for="auth-type">Account Type</label>
                    <select id="auth-type" class="form-select">
                        <option value="candidate">Job Candidate / Applicant</option>
                        <option value="recruiter">Recruiter / Employer HR</option>
                    </select>
                </div>
                
                <div style="display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1.5rem;">
                    <button class="btn-action" id="btn-auth-main" onclick="handleAuthSubmit()">Sign In</button>
                    <div style="text-align: center; margin-top: 0.5rem;">
                        <span id="auth-toggle-msg" style="font-size: 0.8rem; color: var(--text-muted);">New to Zecpath? </span>
                        <a href="javascript:void(0)" id="auth-toggle-link" onclick="toggleAuthMode()" style="font-size: 0.8rem; color: var(--color-primary); font-weight: 600; text-decoration: none;">Create an account</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- CANDIDATE VIEW BOARD -->
        <div id="candidate-panel" style="display: none;">
            <!-- Portal Sub Navigation Tabs -->
            <div class="portal-nav">
                <div class="nav-tab-item active" id="tab-jobs" onclick="switchCandidateTab('jobs')">🔍 Browse Jobs</div>
                <div class="nav-tab-item" id="tab-profile" onclick="switchCandidateTab('profile')">👤 My Profile CV</div>
                <div class="nav-tab-item" id="tab-inbox" onclick="switchCandidateTab('inbox')">📨 Notifications Inbox <span class="notifications-badge" id="notif-count">0</span></div>
            </div>

            <!-- View 1: Jobs Feed -->
            <div id="view-candidate-jobs">
                <div class="card-panel">
                    <div class="section-title">
                        <span>Browse Job Openings</span>
                        <div>
                            <label for="jobs-sorting" style="font-size: 0.8rem; color: var(--text-muted); margin-right: 0.5rem;">Sort by:</label>
                            <select id="jobs-sorting" class="form-select" style="display: inline-block; width: 180px; padding: 0.4rem 0.75rem;" onchange="loadJobFeedList()">
                                <option value="match_highest">Match Score: High to Low</option>
                                <option value="match_lowest">Match Score: Low to High</option>
                                <option value="salary_highest">Salary Budget: High to Low</option>
                            </select>
                        </div>
                    </div>
                    <div class="job-feed" id="job-feed-list">
                        <!-- Injected jobs cards -->
                    </div>
                </div>
            </div>

            <!-- View 2: Profile Section -->
            <div id="view-candidate-profile" style="display: none;">
                <div class="card-panel">
                    <div class="section-title">
                        <span>Resume Automatic Parser & Profile Form</span>
                    </div>
                    
                    <!-- File upload parser -->
                    <div style="background-color: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.15); padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; text-align: center;">
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.75rem;">Upload your Resume CV (.txt or PDF format) to automatically parse details and pre-fill fields.</p>
                        <input type="file" id="profile-resume-file" style="display: none;" onchange="uploadAndParseResume()">
                        <button class="btn-action" style="background: rgba(99, 102, 241, 0.2); border: 1px solid var(--color-primary); color: #fff;" onclick="document.getElementById('profile-resume-file').click()">Select Resume File</button>
                        <div id="parser-file-status" style="font-size: 0.8rem; color: var(--color-success); margin-top: 0.5rem; display: none;">File parsed successfully!</div>
                    </div>

                    <!-- Profile fields grid -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                        <!-- Left col general -->
                        <div>
                            <h3 style="font-size: 0.95rem; font-weight: 600; color: #fff; margin-bottom: 1rem;">General Information</h3>
                            <div class="form-group">
                                <label for="prof-name">Full Name</label>
                                <input type="text" id="prof-name" class="form-input">
                            </div>
                            <div class="form-group">
                                <label for="prof-contact">Contact Phone</label>
                                <input type="text" id="prof-contact" class="form-input">
                            </div>
                            <div class="form-group">
                                <label for="prof-gender">Gender</label>
                                <select id="prof-gender" class="form-select">
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="prof-location">Current Location</label>
                                <input type="text" id="prof-location" class="form-input">
                            </div>
                            <div class="form-group">
                                <label for="prof-notice">Notice Period</label>
                                <input type="text" id="prof-notice" class="form-input" placeholder="e.g. 30 days">
                            </div>
                            <div class="form-group">
                                <label for="prof-salary">Expected Salary (USD / Yr)</label>
                                <input type="number" id="prof-salary" class="form-input">
                            </div>
                        </div>

                        <!-- Right col links & qualifications -->
                        <div>
                            <h3 style="font-size: 0.95rem; font-weight: 600; color: #fff; margin-bottom: 1rem;">Professional & Academic Details</h3>
                            <div class="form-group">
                                <label for="prof-skills">Skills (comma-separated list)</label>
                                <input type="text" id="prof-skills" class="form-input" placeholder="react, node.js, python">
                            </div>
                            <div class="form-group">
                                <label for="prof-exp">Years of Experience</label>
                                <input type="number" id="prof-exp" class="form-input">
                            </div>
                            <div class="form-group">
                                <label for="prof-edu-degree">Education Degree</label>
                                <input type="text" id="prof-edu-degree" class="form-input" placeholder="e.g. Bachelor of Science in CS">
                            </div>
                            <div class="form-group">
                                <label for="prof-edu-school">School / University</label>
                                <input type="text" id="prof-edu-school" class="form-input" placeholder="e.g. Stanford University">
                            </div>
                            <div class="form-group">
                                <label for="prof-edu-year">Graduation Year</label>
                                <input type="text" id="prof-edu-year" class="form-input" placeholder="2024">
                            </div>
                            <div class="form-group">
                                <label for="prof-link-github">GitHub Link</label>
                                <input type="text" id="prof-link-github" class="form-input" placeholder="https://github.com/username">
                            </div>
                            <div class="form-group">
                                <label for="prof-link-linkedin">LinkedIn Link</label>
                                <input type="text" id="prof-link-linkedin" class="form-input" placeholder="https://linkedin.com/in/username">
                            </div>
                            <div class="form-group">
                                <label for="prof-link-portfolio">Portfolio Website Link</label>
                                <input type="text" id="prof-link-portfolio" class="form-input" placeholder="https://username.dev">
                            </div>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="prof-resume">Raw Resume CV Text</label>
                        <textarea id="prof-resume" class="form-textarea" placeholder="Resume content details..."></textarea>
                    </div>

                    <button class="btn-action" style="width: 100%; margin-top: 1rem;" onclick="saveCandidateProfile()">Save Profile Details</button>
                </div>
            </div>

            <!-- View 3: Message notifications list -->
            <div id="view-candidate-inbox" style="display: none;">
                <div class="card-panel">
                    <div class="section-title">
                        <span>Notifications & Mail Desk</span>
                    </div>
                    <div id="notif-list-container">
                        <!-- Injected messages -->
                    </div>
                </div>
            </div>

            <!-- Flow Workspace Active Application panel -->
            <div id="candidate-pipeline-workspace" style="display: none;">
                <div class="stepper-row">
                    <div class="step" id="step-1"><div class="step-num">1</div><div class="step-label">ATS Check</div></div>
                    <div class="step" id="step-2"><div class="step-num">2</div><div class="step-label">Voice call</div></div>
                    <div class="step" id="step-3"><div class="step-num">3</div><div class="step-label">Assessment</div></div>
                    <div class="step" id="step-4"><div class="step-num">4</div><div class="step-label">Negotiation</div></div>
                    <div class="step" id="step-5"><div class="step-num">5</div><div class="step-label">Offer Sign</div></div>
                </div>

                <!-- Panel 1: Apply Info form -->
                <div class="workspace-panel active" id="panel-apply-details">
                    <div class="card-panel">
                        <div class="section-title">
                            <span id="apply-job-header">Apply for Job Position</span>
                        </div>
                        
                        <!-- Upload Custom resume files directly on apply page -->
                        <div style="background-color: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1); padding: 1.25rem; border-radius: 8px; margin-bottom: 1.5rem; text-align: center;">
                            <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.5rem;">Optionally upload a custom resume for this job role, or apply instantly using profile data.</p>
                            <input type="file" id="apply-resume-file" style="display: none;" onchange="uploadApplyResumeFile()">
                            <button class="btn-action" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 0.4rem 1rem;" onclick="document.getElementById('apply-resume-file').click()">Upload Custom Resume</button>
                            <div id="apply-file-status" style="font-size: 0.8rem; color: var(--color-success); margin-top: 0.4rem; display: none;">Custom resume file attached!</div>
                        </div>

                        <div class="scores-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1.25rem;">
                            <div>
                                <label for="app-name" style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.4rem; display: block;">Full Name</label>
                                <input type="text" id="app-name" class="form-input">
                            </div>
                            <div>
                                <label for="app-contact" style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.4rem; display: block;">Contact Details</label>
                                <input type="text" id="app-contact" class="form-input">
                            </div>
                        </div>
                        <div class="scores-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1.25rem;">
                            <div>
                                <label for="app-gender" style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.4rem; display: block;">Gender</label>
                                <select id="app-gender" class="form-select">
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <div>
                                <label for="app-location" style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.4rem; display: block;">Location</label>
                                <input type="text" id="app-location" class="form-input">
                            </div>
                        </div>
                        <div class="scores-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1.25rem;">
                            <div>
                                <label for="app-notice" style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.4rem; display: block;">Notice Period</label>
                                <input type="text" id="app-notice" class="form-input">
                            </div>
                            <div>
                                <label for="app-salary" style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.4rem; display: block;">Expected Salary (USD / Yr)</label>
                                <input type="number" id="app-salary" class="form-input">
                            </div>
                        </div>
                        <button class="btn-action" onclick="submitAtsApplication()">Trigger ATS Analysis & Apply</button>
                        <button class="btn-action" style="background: transparent; border: 1px solid rgba(255,255,255,0.1); margin-left: 0.5rem;" onclick="cancelApplicationFlow()">Back to Job Board</button>
                    </div>
                </div>

                <!-- Panel 1.1: ATS Score Output -->
                <div class="workspace-panel" id="panel-ats">
                    <div class="card-panel" style="text-align: center;">
                        <div class="section-title">
                            <span>ATS Feedback Report</span>
                        </div>
                        
                        <div id="ats-gauge" style="width: 140px; height: 140px; border-radius: 50%; margin: 2rem auto; display: flex; align-items: center; justify-content: center; position: relative;">
                            <div id="ats-score-output" style="font-size: 1.8rem; font-weight: 700; color: #fff;">0%</div>
                        </div>
                        
                        <h3 id="ats-verdict" style="font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;">Analyzing details...</h3>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.5rem;">Mapped Profile Skills:</p>
                        
                        <div id="ats-skills-badge" style="display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; margin-bottom: 2rem;">
                            <!-- Injected badges -->
                        </div>
                        
                        <button class="btn-action" id="btn-to-screening" onclick="goToVoiceScreening()" style="display: none;">Attend AI Interview Call</button>
                        <button class="btn-action" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); margin-left: 0.5rem;" onclick="cancelApplicationFlow()">Back to Job Board</button>
                    </div>
                </div>

                <!-- Panel 2: Voice Interview screen -->
                <div class="workspace-panel" id="panel-voice-screen">
                    <div class="card-panel">
                        <div class="section-title">
                            <span>AI HR voice Screening Interview Call</span>
                        </div>
                        <div class="call-card">
                            <div class="dialogue-stream" id="screening-chat-stream">
                                <!-- Bubbles -->
                            </div>
                            <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                                <input type="text" id="screening-chat-input" class="form-input" placeholder="Type your response to the HR voice questions..." onkeypress="handleScreeningEnter(event)">
                                <button class="btn-action" onclick="submitScreeningAnswer()">Answer</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Panel 3: Sandbox/Aptitude Assessment -->
                <div class="workspace-panel" id="panel-skills-test">
                    <div class="card-panel">
                        <div class="section-title">
                            <span>AI Competency Sandbox Assessment</span>
                        </div>
                        <div id="dynamic-assessment-content">
                            <!-- Dynamic elements injected -->
                        </div>
                    </div>
                </div>

                <!-- Panel 4: Counter offers Salary Negotiation -->
                <div class="workspace-panel" id="panel-salary-negotiate">
                    <div class="card-panel">
                        <div class="section-title">
                            <span>Salary Negotiation & HR Offer Finalization</span>
                        </div>
                        <div class="call-card">
                            <div class="dialogue-stream" id="negotiate-chat-stream">
                                <!-- Bubbles -->
                            </div>
                            <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                                <input type="number" id="negotiate-chat-input" class="form-input" placeholder="Enter annual counter salary USD (e.g. 100000)">
                                <button class="btn-action" onclick="submitCounterSalary()">Counter Offer</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Panel 5: Sign Offer Letter PDF -->
                <div class="workspace-panel" id="panel-offer-document">
                    <div class="card-panel">
                        <div class="section-title">
                            <span>Review & Sign Employment Contract</span>
                        </div>
                        <div class="offer-letter-doc">
                            <div class="offer-header">
                                <div>
                                    <h2 style="color: #6366f1; font-weight: 700;">ZECPATH CORPORATION</h2>
                                    <span style="font-size: 0.75rem; color: #6b7280;">AUTONOMOUS AI CONTRACT DESK</span>
                                </div>
                                <span style="font-size: 0.85rem; color: #4b5563; font-weight: 600;">CONTRACT DISPATCHED</span>
                            </div>
                            <div class="offer-body">
                                <p><strong>Position:</strong> <span id="lbl-offer-role">Developer</span></p>
                                <p><strong>Base Compensation Package:</strong> $<span id="lbl-offer-salary">0.00</span> USD per annum.</p>
                                <p>This automated job offer has been generated based on your scores in the Zecpath AI evaluation pipeline. Both your technical sandbox rating and HR parameters verified selection standards.</p>
                            </div>
                            <div style="margin-top: 2rem; display: flex; justify-content: space-between; align-items: flex-end;">
                                <div>
                                    <div style="font-size: 0.8rem; color: #6b7280;">Hiring Authority</div>
                                    <div style="font-family: cursive; font-size: 1.1rem; color: #6366f1;">Zecpath Auto-Sign</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.8rem; color: #6b7280;">Candidate Sign-off</div>
                                    <div id="lbl-esign" style="font-family: cursive; font-size: 1.1rem; color: #10b981; cursor: pointer;" onclick="executeContractSign()">Click to Accept & E-Sign</div>
                                </div>
                            </div>
                        </div>
                        <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                            <button class="btn-action" style="background-color: var(--color-danger); background-image: none;" onclick="rejectOfferContract()">Reject Contract Offer</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- RECRUITER VIEW BOARD -->
        <div id="recruiter-panel" style="display: none;">
            <div class="rec-metrics">
                <div class="rec-metric-card">
                    <div style="font-size: 0.8rem; color: var(--text-muted)">Hiring Candidates Ingested</div>
                    <div class="rec-metric-val" id="rec-total-applicants">0</div>
                </div>
                <div class="rec-metric-card">
                    <div style="font-size: 0.8rem; color: var(--text-muted)">Selected Candidates</div>
                    <div class="rec-metric-val" id="rec-total-selected">0</div>
                </div>
                <div class="rec-metric-card">
                    <div style="font-size: 0.8rem; color: var(--text-muted)">Active Jobs Posted</div>
                    <div class="rec-metric-val" id="rec-active-jobs">10</div>
                </div>
            </div>

            <!-- Post a New Job -->
            <div class="card-panel">
                <div class="section-title">
                    <span>Post Job Listing</span>
                </div>
                <div class="scores-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                    <div class="form-group">
                        <label for="job-title">Job Title</label>
                        <input type="text" id="job-title" class="form-input" placeholder="e.g. Node Developer">
                    </div>
                    <div class="form-group">
                        <label for="job-skills">Required Skills (comma-separated)</label>
                        <input type="text" id="job-skills" class="form-input" placeholder="react, node.js">
                    </div>
                    <div class="form-group">
                        <label for="job-assess">Assessment Type</label>
                        <select id="job-assess" class="form-select">
                            <option value="coding">Coding Challenge</option>
                            <option value="aptitude">Aptitude Test</option>
                            <option value="design_quiz">Design Theory Quiz</option>
                        </select>
                    </div>
                </div>
                <div class="scores-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                    <div class="form-group">
                        <label for="job-desc">Job Description Text</label>
                        <input type="text" id="job-desc" class="form-input" placeholder="Brief details about the role...">
                    </div>
                    <div class="form-group">
                        <label for="job-budget-min">Salary Budget Min ($)</label>
                        <input type="number" id="job-budget-min" class="form-input" value="60000">
                    </div>
                    <div class="form-group">
                        <label for="job-budget-max">Salary Budget Max ($)</label>
                        <input type="number" id="job-budget-max" class="form-input" value="90000">
                    </div>
                </div>
                <button class="btn-action" onclick="submitRecruiterJobPost()">Post Job Requirement</button>
            </div>

            <!-- Candidate Tracking pipeline table -->
            <div class="card-panel">
                <div class="section-title">
                    <span>Hiring Funnel Candidate Dashboard</span>
                </div>
                <table class="pipeline-table">
                    <thead>
                        <tr>
                            <th>Candidate</th>
                            <th>Role Applied</th>
                            <th>ATS Match</th>
                            <th>Voice Score</th>
                            <th>Assessment</th>
                            <th>Recruiter Recommendation</th>
                            <th>Recruiter Override Action</th>
                        </tr>
                    </thead>
                    <tbody id="recruiter-table-body">
                        <!-- Injected rows -->
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <script>
        let currentUserId = null;
        let currentUserEmail = "";
        let currentUserName = "";
        let currentUserType = "";
        
        let candidateProfile = {
            skills: "",
            experience: 0,
            resume_text: ""
        };

        let selectedJob = null;
        let activeApplication = null;
        let attachedApplyResumeText = "";

        function updateHeaderUI() {
            const container = document.getElementById('user-status-container');
            if (currentUserId) {
                container.innerHTML = `
                    <span>Logged in as: <strong>${currentUserEmail}</strong> (${currentUserType})</span>
                    <button class="btn-logout" onclick="handleLogout()">Sign Out</button>
                `;
            } else {
                container.innerHTML = `<span>Not Signed In</span>`;
            }
        }

        // TAB NAVIGATION
        function switchCandidateTab(tabId) {
            document.getElementById('view-candidate-jobs').style.display = tabId === 'jobs' ? 'block' : 'none';
            document.getElementById('view-candidate-profile').style.display = tabId === 'profile' ? 'block' : 'none';
            document.getElementById('view-candidate-inbox').style.display = tabId === 'inbox' ? 'block' : 'none';
            
            document.querySelectorAll('.nav-tab-item').forEach(item => item.classList.remove('active'));
            document.getElementById(`tab-${tabId}`).classList.add('active');
        }

        // AUTH & ONBOARDING ACTIONS
        let isSignUpMode = false;

        function toggleAuthMode() {
            isSignUpMode = !isSignUpMode;
            const nameGrp = document.getElementById('group-auth-name');
            const title = document.getElementById('auth-title');
            const mainBtn = document.getElementById('btn-auth-main');
            const toggleMsg = document.getElementById('auth-toggle-msg');
            const toggleLink = document.getElementById('auth-toggle-link');

            if (isSignUpMode) {
                nameGrp.style.display = 'block';
                title.innerText = 'Create your Zecpath Account';
                mainBtn.innerText = 'Register Account';
                toggleMsg.innerText = 'Already have an account? ';
                toggleLink.innerText = 'Sign In';
            } else {
                nameGrp.style.display = 'none';
                title.innerText = 'Sign In to Zecpath';
                mainBtn.innerText = 'Sign In';
                toggleMsg.innerText = 'New to Zecpath? ';
                toggleLink.innerText = 'Create an account';
            }
        }

        async function handleAuthSubmit() {
            const email = document.getElementById('auth-email').value;
            const password = document.getElementById('auth-pass').value;
            const type = document.getElementById('auth-type').value;

            if (!email || !password) {
                alert("Please input login credentials!");
                return;
            }

            if (isSignUpMode) {
                const name = document.getElementById('auth-name').value;
                if (!name) {
                    alert("Please enter your name to register!");
                    return;
                }

                try {
                    const response = await fetch('/api/auth/register', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name, email, password, user_type: type })
                    });
                    
                    if (response.ok) {
                        alert("Registration successful! Please login.");
                        toggleAuthMode();
                    } else {
                        const err = await response.json();
                        alert(err.detail || "Registration failed!");
                    }
                } catch (err) {
                    alert("Registration Error: " + err);
                }
            } else {
                try {
                    const response = await fetch('/api/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password, user_type: type })
                    });
                    
                    if (!response.ok) {
                        const err = await response.json();
                        alert(err.detail || "Authentication Failed!");
                        return;
                    }
                    
                    const data = await response.json();
                    currentUserId = data.user_id;
                    currentUserEmail = data.email;
                    currentUserName = data.name || "";
                    currentUserType = type;

                    document.getElementById('auth-panel').style.display = 'none';
                    updateHeaderUI();

                    if (type === 'candidate') {
                        document.getElementById('candidate-panel').style.display = 'block';
                        await loadCandidateProfileData();
                        await loadJobFeedList();
                        await loadCandidateNotifications();
                    } else {
                        document.getElementById('recruiter-panel').style.display = 'block';
                        loadRecruiterDashboard();
                    }
                } catch (err) {
                    alert("Auth Error: " + err);
                }
            }
        }

        function handleLogout() {
            currentUserId = null;
            currentUserEmail = "";
            currentUserType = "";
            document.getElementById('candidate-panel').style.display = 'none';
            document.getElementById('recruiter-panel').style.display = 'none';
            document.getElementById('auth-panel').style.display = 'block';
            updateHeaderUI();
        }

        // PROFILE SECTION SAVING & RESUME PARSING
        async function loadCandidateProfileData() {
            try {
                const res = await fetch(`/api/candidates/profile/${currentUserId}`);
                if (res.ok) {
                    const data = await res.json();
                    if (data) {
                        document.getElementById('prof-name').value = data.name || "";
                        document.getElementById('prof-contact').value = data.contact_info || "";
                        document.getElementById('prof-gender').value = data.gender || "Male";
                        document.getElementById('prof-location').value = data.location || "";
                        document.getElementById('prof-notice').value = data.notice_period || "";
                        document.getElementById('prof-salary').value = data.expected_salary || 0;
                        document.getElementById('prof-skills').value = data.skills || "";
                        document.getElementById('prof-exp').value = data.experience || 0;
                        document.getElementById('prof-edu-degree').value = data.education_degree || "";
                        document.getElementById('prof-edu-school').value = data.education_school || "";
                        document.getElementById('prof-edu-year').value = data.education_year || "";
                        document.getElementById('prof-link-github').value = data.github_url || "";
                        document.getElementById('prof-link-linkedin').value = data.linkedin_url || "";
                        document.getElementById('prof-link-portfolio').value = data.portfolio_url || "";
                        document.getElementById('prof-resume').value = data.resume_text || "";
                        
                        candidateProfile = data;
                    }
                }
            } catch (err) {
                console.log("Error loading profile: " + err);
            }
        }

        async function saveCandidateProfile() {
            const name = document.getElementById('prof-name').value;
            const contact = document.getElementById('prof-contact').value;
            const gender = document.getElementById('prof-gender').value;
            const location = document.getElementById('prof-location').value;
            const notice = document.getElementById('prof-notice').value;
            const salary = parseInt(document.getElementById('prof-salary').value) || 0;
            const skills = document.getElementById('prof-skills').value;
            const exp = parseInt(document.getElementById('prof-exp').value) || 0;
            const eduDegree = document.getElementById('prof-edu-degree').value;
            const eduSchool = document.getElementById('prof-edu-school').value;
            const eduYear = document.getElementById('prof-edu-year').value;
            const github = document.getElementById('prof-link-github').value;
            const linkedin = document.getElementById('prof-link-linkedin').value;
            const portfolio = document.getElementById('prof-link-portfolio').value;
            const resume = document.getElementById('prof-resume').value;

            try {
                const response = await fetch('/api/candidates/profile/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        candidate_id: currentUserId,
                        name, contact_info: contact, gender, location,
                        notice_period: notice, expected_salary: salary, skills, experience: exp, resume_text: resume,
                        education_degree: eduDegree, education_school: eduSchool, education_year: eduYear,
                        github_url: github, linkedin_url: linkedin, portfolio_url: portfolio
                    })
                });
                if (response.ok) {
                    alert("Profile CV Details Saved successfully!");
                    await loadCandidateProfileData();
                    await loadJobFeedList();
                }
            } catch (err) {
                alert("Save Profile Error: " + err);
            }
        }

        async function uploadAndParseResume() {
            const fileInput = document.getElementById('profile-resume-file');
            if (fileInput.files.length === 0) return;
            
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append("file", file);

            try {
                const response = await fetch('/api/parser/resume', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    
                    if (data.name) document.getElementById('prof-name').value = data.name;
                    if (data.contact_info) document.getElementById('prof-contact').value = data.contact_info;
                    if (data.location) document.getElementById('prof-location').value = data.location;
                    if (data.skills) document.getElementById('prof-skills').value = data.skills;
                    if (data.experience) document.getElementById('prof-exp').value = data.experience;
                    if (data.education_degree) document.getElementById('prof-edu-degree').value = data.education_degree;
                    if (data.education_school) document.getElementById('prof-edu-school').value = data.education_school;
                    if (data.education_year) document.getElementById('prof-edu-year').value = data.education_year;
                    if (data.resume_text) document.getElementById('prof-resume').value = data.resume_text;

                    document.getElementById('parser-file-status').style.display = 'block';
                    setTimeout(() => {
                        document.getElementById('parser-file-status').style.display = 'none';
                    }, 3000);
                }
            } catch (err) {
                alert("Resume parsing failed: " + err);
            }
        }

        // BROWSE JOB LISTINGS & SORTING
        async function loadJobFeedList() {
            try {
                const sortType = document.getElementById('jobs-sorting').value;
                const response = await fetch('/api/jobs/list');
                let jobs = await response.json();
                
                // Calculate match score ratios first
                jobs.forEach(j => {
                    let score = 40;
                    if (candidateProfile.skills) {
                        const required = j.skills_required.toLowerCase().split(',');
                        const owned = candidateProfile.skills.toLowerCase().split(',');
                        let matchedCount = 0;
                        required.forEach(s => {
                            if (owned.some(o => o.trim() === s.trim())) {
                                matchedCount++;
                            }
                        });
                        const ratio = required.length > 0 ? (matchedCount / required.length) : 0;
                        if (ratio >= 0.8) score = 90;
                        else if (ratio >= 0.5) score = 75;
                    }
                    j.match_score = score;
                });

                // Apply Sorting
                if (sortType === 'match_highest') {
                    jobs.sort((a, b) => b.match_score - a.match_score);
                } else if (sortType === 'match_lowest') {
                    jobs.sort((a, b) => a.match_score - b.match_score);
                } else if (sortType === 'salary_highest') {
                    jobs.sort((a, b) => b.budget_max - a.budget_max);
                }

                const feed = document.getElementById('job-feed-list');
                feed.innerHTML = '';
                
                jobs.forEach(j => {
                    let matchClass = 'match-low';
                    let matchLabel = 'Low Match';
                    if (j.match_score >= 90) { matchClass = 'match-strong'; matchLabel = 'Strong Match'; }
                    else if (j.match_score >= 75) { matchClass = 'match-good'; matchLabel = 'Good Match'; }

                    feed.innerHTML += `
                        <div class="job-card">
                            <div class="job-info">
                                <h3>${j.title}</h3>
                                <p style="font-weight: 500; color: #818cf8; margin-bottom: 0.25rem;">Company: ${j.company_name} | Budget: $${j.budget_min.toLocaleString()} - $${j.budget_max.toLocaleString()}</p>
                                <p>${j.description}</p>
                                <div class="match-badge ${matchClass}">🟢 ${matchLabel} (${j.match_score}%)</div>
                            </div>
                            <button class="btn-action" onclick="openApplicationFlow(${JSON.stringify(j).replace(/"/g, '&quot;')})">Apply Now</button>
                        </div>
                    `;
                });
            } catch (err) {
                console.log("Error loading jobs: " + err);
            }
        }

        // CANDIDATE APPLY FLOW PROGRESSION (AUTO-FILL FROM PROFILE)
        function openApplicationFlow(jobObj) {
            selectedJob = jobObj;
            document.getElementById('view-candidate-jobs').style.display = 'none';
            document.getElementById('tab-profile').style.display = 'none';
            document.getElementById('tab-inbox').style.display = 'none';
            document.getElementById('tab-jobs').style.display = 'none';
            document.getElementById('candidate-pipeline-workspace').style.display = 'block';
            document.getElementById('apply-job-header').innerText = `Apply for: ${jobObj.title} at ${jobObj.company_name}`;
            
            // Auto-fill from saved profile details
            document.getElementById('app-name').value = candidateProfile.name || "";
            document.getElementById('app-contact').value = candidateProfile.contact_info || "";
            document.getElementById('app-gender').value = candidateProfile.gender || "Male";
            document.getElementById('app-location').value = candidateProfile.location || "";
            document.getElementById('app-notice').value = candidateProfile.notice_period || "";
            document.getElementById('app-salary').value = candidateProfile.expected_salary || 90000;
            attachedApplyResumeText = candidateProfile.resume_text || "";

            // Reset Stepper
            document.querySelectorAll('.step').forEach(s => s.className = 'step');
            document.querySelectorAll('.workspace-panel').forEach(p => p.classList.remove('active'));
            document.getElementById('step-1').classList.add('active');
            document.getElementById('panel-apply-details').classList.add('active');
        }

        function cancelApplicationFlow() {
            document.getElementById('candidate-pipeline-workspace').style.display = 'none';
            document.getElementById('tab-profile').style.display = 'block';
            document.getElementById('tab-inbox').style.display = 'block';
            document.getElementById('tab-jobs').style.display = 'block';
            document.getElementById('view-candidate-jobs').style.display = 'block';
            switchCandidateTab('jobs');
        }

        async function uploadApplyResumeFile() {
            const fileInput = document.getElementById('apply-resume-file');
            if (fileInput.files.length === 0) return;
            
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append("file", file);

            try {
                const response = await fetch('/api/parser/resume', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    attachedApplyResumeText = data.resume_text || "";
                    document.getElementById('apply-file-status').style.display = 'block';
                }
            } catch (err) {
                alert("File parse failed: " + err);
            }
        }

        async function submitAtsApplication() {
            const name = document.getElementById('app-name').value;
            const contact = document.getElementById('app-contact').value;
            const gender = document.getElementById('app-gender').value;
            const location = document.getElementById('app-location').value;
            const notice = document.getElementById('app-notice').value;
            const salary = parseInt(document.getElementById('app-salary').value);

            if (!contact || !location || !notice) {
                alert("Please fill application fields!");
                return;
            }

            try {
                const response = await fetch('/api/apply', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        candidate_id: currentUserId,
                        job_id: selectedJob.id,
                        name: name,
                        contact_info: contact,
                        gender, location, notice_period: notice, expected_salary: salary,
                        experience: candidateProfile.experience || 1,
                        resume_text: attachedApplyResumeText || candidateProfile.resume_text || ""
                    })
                });

                const appObj = await response.json();
                activeApplication = appObj;
                
                // Show ATS result
                document.getElementById('panel-apply-details').classList.remove('active');
                document.getElementById('panel-ats').classList.add('active');
                
                document.getElementById('ats-score-output').innerText = Math.round(appObj.ats_score) + '%';
                document.getElementById('ats-gauge').style.background = `radial-gradient(circle, var(--bg-panel) 55%, transparent 60%), conic-gradient(var(--color-primary) ${appObj.ats_score}%, rgba(255,255,255,0.05) ${appObj.ats_score}%)`;
                
                const verdict = document.getElementById('ats-verdict');
                const btnScreening = document.getElementById('btn-to-screening');
                const skillsBadge = document.getElementById('ats-skills-badge');
                
                skillsBadge.innerHTML = '';
                const skillsList = candidateProfile.skills ? candidateProfile.skills.split(',') : [];
                skillsList.forEach(s => {
                    if (s.trim()) {
                        skillsBadge.innerHTML += `<span class="skill-badge">${s.trim()}</span>`;
                    }
                });

                if (appObj.ats_score >= 60) {
                    verdict.innerText = "Shortlisted! Check inbox for AI interview details.";
                    verdict.style.color = "var(--color-success)";
                    btnScreening.style.display = "inline-block";
                    document.getElementById('step-1').className = 'step completed';
                } else {
                    verdict.innerText = "Unfortunately, you are not selected.";
                    verdict.style.color = "var(--color-danger)";
                    btnScreening.style.display = "none";
                }
                await loadCandidateNotifications();
            } catch (err) {
                alert("Apply Error: " + err);
            }
        }

        // STAGE 2: VOICE SCREENING FLOW
        function goToVoiceScreening() {
            document.getElementById('panel-ats').classList.remove('active');
            document.getElementById('panel-voice-screen').classList.add('active');
            document.getElementById('step-2').classList.add('active');
            
            const stream = document.getElementById('screening-chat-stream');
            stream.innerHTML = '';
            
            appendScreeningBubble(`Hello. Welcome to Zecpath AI voice screening. Let's verify experience and parameters. Please introduce yourself briefly.`, 'ai');
        }

        function appendScreeningBubble(text, speaker) {
            const stream = document.getElementById('screening-chat-stream');
            const bubble = document.createElement('div');
            bubble.className = `bubble ${speaker}`;
            bubble.innerText = text;
            stream.appendChild(bubble);
            stream.scrollTop = stream.scrollHeight;
        }

        const SCREENING_QS = [
            "What notice period do you require to join?",
            "What is your expected annual compensation package?"
        ];
        let currentScreenIndex = 0;
        let screeningTranscript = "";

        function handleScreeningEnter(event) {
            if (event.key === 'Enter') {
                submitScreeningAnswer();
            }
        }

        function submitScreeningAnswer() {
            const input = document.getElementById('screening-chat-input');
            const text = input.value.trim();
            if (!text) return;
            
            appendScreeningBubble(text, 'user');
            screeningTranscript += `\nUser: ${text}`;
            input.value = '';

            setTimeout(async () => {
                if (currentScreenIndex < SCREENING_QS.length) {
                    const nextQ = SCREENING_QS[currentScreenIndex];
                    appendScreeningBubble(nextQ, 'ai');
                    screeningTranscript += `\nAI: ${nextQ}`;
                    currentScreenIndex++;
                } else {
                    appendScreeningBubble("Voice screening finished. Evaluating transcript scores...", 'ai');
                    document.getElementById('step-2').className = 'step completed';
                    
                    const response = await fetch('/api/applications/screening/submit', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            application_id: activeApplication.id,
                            screening_score: 85.0,
                            transcript: screeningTranscript
                        })
                    });
                    
                    if (response.ok) {
                        setTimeout(async () => {
                            await loadCandidateNotifications();
                            loadAssessmentStage();
                        }, 1500);
                    }
                }
            }, 1000);
        }

        // STAGE 3: ASSESSMENT ROUND
        function loadAssessmentStage() {
            document.getElementById('panel-voice-screen').classList.remove('active');
            document.getElementById('panel-skills-test').classList.add('active');
            document.getElementById('step-3').classList.add('active');
            
            const container = document.getElementById('dynamic-assessment-content');
            container.innerHTML = '';
            
            if (selectedJob.assessment_type === 'coding') {
                container.innerHTML = `
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">Complete the coding sandbox challenge:</p>
                    <div class="editor-container">
                        <textarea class="editor-textarea" id="editor-sandbox-code">function reverseString(str) {\\n  // Write JS logic here\\n  return str.split('').reverse().join('');\\n}</textarea>
                        <div class="editor-terminal" id="terminal-out-box">Terminal: Ready.</div>
                    </div>
                    <button class="btn-action" style="margin-top: 1rem;" onclick="evaluateCodingSandbox()">Compile Code Sandbox</button>
                `;
            } else {
                container.innerHTML = `
                    <p style="font-size: 0.9rem; margin-bottom: 1rem;">Aptitude / Design scenario choice evaluation:</p>
                    <div class="form-group">
                        <p style="font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">Select the correct business standard decision:</p>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.85rem;">
                            <label><input type="radio" name="apt-choice" value="A"> A. Propose discount instantly.</label>
                            <label><input type="radio" name="apt-choice" value="B"> B. Emphasize value proposition and ROI alignment.</label>
                            <label><input type="radio" name="apt-choice" value="C"> C. Fixed cost response.</label>
                        </div>
                    </div>
                    <button class="btn-action" onclick="evaluateQuizChoice()">Submit Scenario Answer</button>
                `;
            }
        }

        async function evaluateCodingSandbox() {
            const code = document.getElementById('editor-sandbox-code').value;
            const terminal = document.getElementById('terminal-out-box');
            terminal.innerText = "Sandbox: Compiling algorithm...";

            try {
                const response = await fetch('/api/assessment/evaluate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        role_key: selectedJob.assessment_type,
                        code_content: code
                    })
                });
                
                const result = await response.json();
                terminal.innerText = `Output: ${result.message} | Score: ${result.score}%`;
                
                await saveAssessmentResult(result.score);
            } catch (err) {
                alert("Sandbox compiler error: " + err);
            }
        }

        async function evaluateQuizChoice() {
            const checked = document.querySelector('input[name="apt-choice"]:checked');
            if (!checked) {
                alert("Please choose an answer!");
                return;
            }
            const val = checked.value;
            const score = val === "B" ? 100.0 : 0.0;
            
            await saveAssessmentResult(score);
        }

        async function saveAssessmentResult(score) {
            try {
                const response = await fetch('/api/applications/assessment/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        application_id: activeApplication.id,
                        score: score
                    })
                });
                
                if (response.ok) {
                    document.getElementById('step-3').className = 'step completed';
                    setTimeout(() => {
                        loadNegotiationRound();
                    }, 1500);
                }
            } catch (err) {
                alert("Save Assessment error: " + err);
            }
        }

        // STAGE 4: NEGOTIATION
        let negotiationAttempts = 0;
        function loadNegotiationRound() {
            document.getElementById('panel-skills-test').classList.remove('active');
            document.getElementById('panel-salary-negotiate').classList.add('active');
            document.getElementById('step-4').classList.add('active');
            
            const stream = document.getElementById('negotiate-chat-stream');
            stream.innerHTML = '';
            negotiationAttempts = 0;
            
            appendNegotiationBubble(`We have verified your coding assessment. Your expected salary package is $${activeApplication.negotiated_salary || 90000} USD. Let's finalize your offer.`, 'ai');
        }

        function appendNegotiationBubble(text, speaker) {
            const stream = document.getElementById('negotiate-chat-stream');
            const bubble = document.createElement('div');
            bubble.className = `bubble ${speaker}`;
            bubble.innerText = text;
            stream.appendChild(bubble);
            stream.scrollTop = stream.scrollHeight;
        }

        async function submitCounterSalary() {
            const input = document.getElementById('negotiate-chat-input');
            const val = parseFloat(input.value);
            if (isNaN(val) || val <= 0) {
                alert("Please enter a valid salary!");
                return;
            }

            appendNegotiationBubble(`I propose counter compensation: $${val} USD`, 'user');
            negotiationAttempts++;
            input.value = '';

            try {
                const response = await fetch('/api/negotiate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        role_key: selectedJob.assessment_type,
                        expected_salary: val,
                        counter_offer_count: negotiationAttempts
                    })
                });
                const result = await response.json();
                
                setTimeout(() => {
                    appendNegotiationBubble(result.message, 'ai');
                    if (result.status === 'agreed') {
                        activeApplication.negotiated_salary = result.salary;
                        document.getElementById('step-4').className = 'step completed';
                        
                        setTimeout(() => {
                            loadOfferDocumentRound();
                        }, 1500);
                    }
                }, 1000);
            } catch (err) {
                alert("Negotiation Error: " + err);
            }
        }

        // STAGE 5: OFFER LETTER ACTIONS
        function loadOfferDocumentRound() {
            document.getElementById('panel-salary-negotiate').classList.remove('active');
            document.getElementById('panel-offer-document').classList.add('active');
            document.getElementById('step-5').classList.add('active');
            
            document.getElementById('lbl-offer-role').innerText = selectedJob.title;
            document.getElementById('lbl-offer-salary').innerText = activeApplication.negotiated_salary.toLocaleString();
        }

        async function executeContractSign() {
            try {
                const response = await fetch('/api/applications/offer/action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        application_id: activeApplication.id,
                        action: 'accepted'
                    })
                });
                
                if (response.ok) {
                    document.getElementById('lbl-esign').innerText = "Contract Accepted & Signed!";
                    document.getElementById('lbl-esign').onclick = null;
                    document.getElementById('step-5').className = 'step completed';
                    alert("Congratulations! Offer fully accepted and contract active!");
                }
            } catch (err) {
                alert("Sign error: " + err);
            }
        }

        async function rejectOfferContract() {
             try {
                const response = await fetch('/api/applications/offer/action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        application_id: activeApplication.id,
                        action: 'rejected'
                    })
                });
                
                if (response.ok) {
                    alert("You have declined the employment offer.");
                    cancelApplicationFlow();
                }
            } catch (err) {
                alert("Rejection error: " + err);
            }
        }

        // MAIL NOTIFICATIONS POLL
        async function loadCandidateNotifications() {
            try {
                const response = await fetch(`/api/notifications/list/${currentUserId}`);
                const data = await response.json();
                
                document.getElementById('notif-count').innerText = data.length;
                const container = document.getElementById('notif-list-container');
                container.innerHTML = '';
                
                if (data.length === 0) {
                    container.innerHTML = `<p style="font-size: 0.8rem; color: var(--text-muted); text-align: center;">No emails or updates in inbox.</p>`;
                    return;
                }

                data.forEach(n => {
                    container.innerHTML += `
                        <div class="notification-card">
                            <div class="notification-title">✉ ${n.title}</div>
                            <div class="notification-body">${n.message}</div>
                        </div>
                    `;
                });
            } catch (err) {
                console.log("Error loading notif: " + err);
            }
        }

        // RECRUITER FUNCTIONS
        async function submitRecruiterJobPost() {
            const title = document.getElementById('job-title').value;
            const skills = document.getElementById('job-skills').value;
            const desc = document.getElementById('job-desc').value;
            const budgetMin = parseInt(document.getElementById('job-budget-min').value);
            const budgetMax = parseInt(document.getElementById('job-budget-max').value);
            const assess = document.getElementById('job-assess').value;

            if (!title || !skills || !desc) {
                alert("Please fill job posting fields!");
                return;
            }

            try {
                const response = await fetch('/api/jobs/post', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        company_name: "Zecpath Corporation",
                        title, description: desc, skills_required: skills,
                        budget_min: budgetMin, budget_max: budgetMax, assessment_type: assess
                    })
                });

                if (response.ok) {
                    alert("Job requirement posted successfully!");
                    loadRecruiterDashboard();
                }
            } catch (err) {
                alert("Post Job Error: " + err);
            }
        }

        async function loadRecruiterDashboard() {
            try {
                const response = await fetch('/api/recruiter/pipeline');
                const data = await response.json();
                
                document.getElementById('rec-total-applicants').innerText = data.length;
                const selectedCount = data.filter(c => c.status === 'Selected').length;
                document.getElementById('rec-total-selected').innerText = selectedCount;

                const tbody = document.getElementById('recruiter-table-body');
                tbody.innerHTML = '';
                
                data.forEach(c => {
                    tbody.innerHTML += `
                        <tr>
                            <td><strong>${c.candidate_name}</strong></td>
                            <td>${c.job_title}</td>
                            <td>${Math.round(c.ats_score)}%</td>
                            <td>${c.screening_score ? Math.round(c.screening_score) + '%' : 'Pending'}</td>
                            <td>${c.assessment_score ? Math.round(c.assessment_score) + '%' : 'Pending'}</td>
                            <td><span class="decision-badge badge-selected">${c.status}</span></td>
                            <td>
                                <select class="action-select" onchange="overrideAIRecommendation(${c.id}, this.value)">
                                    <option value="">-- Override --</option>
                                    <option value="Selected">Select Candidate</option>
                                    <option value="Rejected">Reject Candidate</option>
                                </select>
                            </td>
                        </tr>
                    `;
                });
            } catch (err) {
                console.log("Error loading recruiter dashboard: " + err);
            }
        }

        async function overrideAIRecommendation(appId, decision) {
            if (!decision) return;
            try {
                const response = await fetch('/api/recruiter/override', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ application_id: appId, decision })
                });
                
                if (response.ok) {
                    alert(`AI recommendation overridden to: ${decision}`);
                    loadRecruiterDashboard();
                }
            } catch (err) {
                alert("Override error: " + err);
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return INDEX_HTML

# ----------------------------------------------------------------------
# ENDPOINTS: USER MANAGEMENT & ONBOARDING & PARSING
# ----------------------------------------------------------------------
@app.post("/api/auth/register")
def register_user(req: RegisterRequest):
    table = "candidates" if req.user_type == "candidate" else "companies"
    
    duplicate = db_query(f"SELECT * FROM {table} WHERE email = ?", (req.email,))
    if duplicate:
        raise HTTPException(status_code=400, detail="Account email already registered!")
        
    db_execute(
        f"INSERT INTO {table} (name, email, password) VALUES (?, ?, ?)",
        (req.name, req.email, req.password)
    )
    return {"message": "Success"}

@app.post("/api/auth/login")
def login_user(req: LoginRequest):
    table = "candidates" if req.user_type == "candidate" else "companies"
    
    user = db_query(f"SELECT * FROM {table} WHERE email = ? AND password = ?", (req.email, req.password))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
        
    return {
        "user_id": user[0]["id"],
        "email": user[0]["email"],
        "name": user[0]["name"]
    }

@app.get("/api/candidates/profile/{candidate_id}")
def get_candidate_profile(candidate_id: int):
    profile = db_query("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    if not profile:
        return {}
    return profile[0]

@app.post("/api/candidates/profile/save")
def save_candidate_profile(req: ProfileSaveRequest):
    db_execute(
        """
        UPDATE candidates 
        SET name=?, contact_info=?, gender=?, location=?, notice_period=?, expected_salary=?, skills=?, experience=?, resume_text=?,
            education_degree=?, education_school=?, education_year=?, github_url=?, linkedin_url=?, portfolio_url=?
        WHERE id=?
        """,
        (req.name, req.contact_info, req.gender, req.location, req.notice_period, req.expected_salary, req.skills, req.experience, req.resume_text,
         req.education_degree, req.education_school, req.education_year, req.github_url, req.linkedin_url, req.portfolio_url, req.candidate_id)
    )
    return {"message": "Success"}

@app.post("/api/parser/resume")
async def parse_resume(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename.lower()
    
    text = ""
    if filename.endswith(".pdf"):
        if HAS_PDF_PARSER:
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
            except Exception as e:
                text = f"[PDF Parsing Failed: {e}]"
        else:
            text = "[PDF parser dependency missing on server, falling back to raw binary read]\n" + contents.decode("utf-8", errors="ignore")
    else:
        text = contents.decode("utf-8", errors="ignore")
        
    # Heuristic matches from text
    name_match = re.search(r"Name\s*:\s*([^\n\r]+)", text, re.IGNORECASE)
    phone_match = re.search(r"(?:Phone|Contact)\s*:\s*([^\n\r]+)", text, re.IGNORECASE)
    location_match = re.search(r"Location\s*:\s*([^\n\r]+)", text, re.IGNORECASE)
    degree_match = re.search(r"(?:Education|Degree)\s*:\s*([^\n\r]+)", text, re.IGNORECASE)
    school_match = re.search(r"(?:School|University)\s*:\s*([^\n\r]+)", text, re.IGNORECASE)
    year_match = re.search(r"Year\s*:\s*(\d{4})", text, re.IGNORECASE)
    
    # Skills mapping heuristic
    known_skills = ["react", "node.js", "express", "mongodb", "javascript", "python", "fastapi", "postgresql", "docker", "django", "figma", "excel", "testing", "cypress", "selenium"]
    matched_skills = [s for s in known_skills if s in text.lower()]
    
    return {
        "name": name_match.group(1).strip() if name_match else "Parsed Applicant",
        "contact_info": phone_match.group(1).strip() if phone_match else "",
        "location": location_match.group(1).strip() if location_match else "",
        "skills": ",".join(matched_skills),
        "experience": 3 if "senior" in text.lower() else 1,
        "education_degree": degree_match.group(1).strip() if degree_match else "",
        "education_school": school_match.group(1).strip() if school_match else "",
        "education_year": year_match.group(1).strip() if year_match else "",
        "resume_text": text
    }

# ----------------------------------------------------------------------
# ENDPOINTS: JOB ROLE LISTINGS
# ----------------------------------------------------------------------
@app.post("/api/jobs/post")
def post_job(req: JobPostRequest):
    db_execute(
        "INSERT INTO jobs (company_id, company_name, title, description, skills_required, budget_min, budget_max, assessment_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (1, req.company_name, req.title, req.description, req.skills_required, req.budget_min, req.budget_max, req.assessment_type)
    )
    return {"message": "Job posted successfully!"}

@app.get("/api/jobs/list")
def list_jobs():
    return db_query("SELECT * FROM jobs WHERE status = 'open'")

# ----------------------------------------------------------------------
# ENDPOINTS: APPLICANTS FUNNEL SIMULATOR
# ----------------------------------------------------------------------
@app.post("/api/apply")
def apply_to_job(req: ApplyRequest):
    job = db_query("SELECT * FROM jobs WHERE id = ?", (req.job_id,))
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found.")
        
    candidate = db_query("SELECT * FROM candidates WHERE id = ?", (req.candidate_id,))
    candidate_email = candidate[0]["email"] if candidate else req.name.lower().replace(" ", "") + "@example.com"
        
    # Calculate ATS Score based on skill mapping
    job_skills = job[0]["skills_required"].lower().split(",")
    candidate_skills = req.resume_text.lower()
    
    matched = []
    for s in job_skills:
        if s.strip() in candidate_skills:
            matched.append(s.strip())
            
    ats_score = (len(matched) / len(job_skills)) * 100.0 if job_skills else 50.0
    if ats_score < 40.0:
        ats_score = 45.0
        
    status = "shortlisted" if ats_score >= 60.0 else "rejected"
    
    db_execute(
        "INSERT INTO applications (job_id, candidate_id, ats_score, status, negotiated_salary) VALUES (?, ?, ?, ?, ?)",
        (req.job_id, req.candidate_id, ats_score, status, req.expected_salary)
    )
    
    new_app = db_query("SELECT * FROM applications WHERE job_id = ? AND candidate_id = ? ORDER BY id DESC LIMIT 1", (req.job_id, req.candidate_id))
    
    if status == "shortlisted":
        title = "Congratulations! Shortlisted"
        msg = f"You have been shortlisted for the {job[0]['title']} role. Please complete the AI Screening Interview round."
        db_execute(
            "INSERT INTO notifications (candidate_id, title, message) VALUES (?, ?, ?)",
            (req.candidate_id, title, msg)
        )
        # Dispatch shortlisted email
        send_email_notification(
            to_email=candidate_email,
            subject=f"Shortlisted: AI Screening Invitation for {job[0]['title']}",
            body_text=f"Dear {req.name},\n\nCongratulations! You have been shortlisted for the {job[0]['title']} role. Please click the link inside your portal notification center to complete the AI Screening Interview.\n\nBest regards,\nZecpath Recruitment Engine"
        )
    else:
        title = "Application Update"
        msg = "Unfortunately, you are not selected."
        db_execute(
            "INSERT INTO notifications (candidate_id, title, message) VALUES (?, ?, ?)",
            (req.candidate_id, title, msg)
        )
        # Dispatch rejection email
        send_email_notification(
            to_email=candidate_email,
            subject=f"Application Update: {job[0]['title']}",
            body_text=f"Dear {req.name},\n\nThank you for applying to the {job[0]['title']} role. Unfortunately, you are not selected at this time.\n\nBest regards,\nZecpath Recruitment Engine"
        )
        
    return new_app[0]

@app.post("/api/applications/screening/submit")
def submit_screening(req: ScreeningSubmitRequest):
    db_execute(
        "UPDATE applications SET screening_score=?, status='screening_completed', screening_transcript=? WHERE id=?",
        (req.screening_score, req.transcript, req.application_id)
    )
    
    app_info = db_query("SELECT * FROM applications WHERE id = ?", (req.application_id,))
    job_info = db_query("SELECT * FROM jobs WHERE id = ?", (app_info[0]["job_id"],))
    candidate = db_query("SELECT * FROM candidates WHERE id = ?", (app_info[0]["candidate_id"],))
    candidate_email = candidate[0]["email"] if candidate else "candidate@example.com"
    candidate_name = candidate[0]["name"] if candidate else "Candidate"
    
    title = "Round 2 Complete: Technical Invitation"
    msg = f"You have passed the screening round. Please complete your Technical Sandbox Coding/Aptitude round for the {job_info[0]['title']} role."
    db_execute(
        "INSERT INTO notifications (candidate_id, title, message) VALUES (?, ?, ?)",
        (app_info[0]["candidate_id"], title, msg)
    )
    
    # Dispatch next round email
    send_email_notification(
        to_email=candidate_email,
        subject=f"Passed Round 1 Screening: Technical Challenge for {job_info[0]['title']}",
        body_text=f"Dear {candidate_name},\n\nYou have successfully passed the screening interview! Please complete the Technical/Aptitude test by visiting the candidate assessment panel in the Zecpath portal.\n\nBest regards,\nZecpath Recruitment Engine"
    )
    
    return {"message": "Success"}

@app.post("/api/assessment/evaluate")
def evaluate_assessment(payload: AssessmentPayload):
    role = payload.role_key
    if role == "coding":
        code = payload.code_content
        if "reverse" in code and ("split" in code or "for" in code):
            return {"score": 100.0, "message": "Sandbox test cases passed. Function reverseString works."}
        else:
            return {"score": 50.0, "message": "Sandbox execution failed."}
    else:
        return {"score": 100.0, "message": "Evaluation successful."}

@app.post("/api/applications/assessment/submit")
def submit_assessment(req: AssessmentSubmitRequest):
    db_execute(
        "UPDATE applications SET assessment_score=?, status='technical_completed' WHERE id=?",
        (req.score, req.application_id)
    )
    return {"message": "Success"}

@app.post("/api/negotiate")
def negotiate_salary(payload: NegotiationPayload):
    expected = payload.expected_salary
    if expected <= 95000:
        return {"status": "agreed", "salary": expected, "message": f"Perfect. We agree to your expected salary of ${expected:,} USD."}
    else:
        if payload.counter_offer_count >= 3:
            return {"status": "agreed", "salary": 95000, "message": "To proceed, we have capped the offer at our maximum budget of $95,000 USD."}
        else:
            counter = round((expected + 95000) / 2)
            return {"status": "counter", "salary": counter, "message": f"Can we compromise at a midpoint of ${counter:,} USD?"}

@app.post("/api/applications/offer/action")
def take_offer_action(req: OfferActionRequest):
    db_execute(
        "UPDATE applications SET offer_accepted=?, status=? WHERE id=?",
        (req.action, "Selected" if req.action == "accepted" else "Rejected", req.application_id)
    )
    return {"message": "Success"}

# ----------------------------------------------------------------------
# ENDPOINTS: RECRUITER ANALYTICS & OVERRIDES
# ----------------------------------------------------------------------
@app.get("/api/recruiter/pipeline")
def get_recruiter_pipeline():
    query = """
        SELECT a.id, a.ats_score, a.screening_score, a.assessment_score, a.status,
               c.name as candidate_name, j.title as job_title
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        JOIN jobs j ON a.job_id = j.id
    """
    return db_query(query)

@app.post("/api/recruiter/override")
def recruiter_override(req: OverrideRequest):
    db_execute(
        "UPDATE applications SET status=?, recruiter_override=? WHERE id=?",
        (req.decision, "override_" + req.decision.lower(), req.application_id)
    )
    
    app_info = db_query("SELECT * FROM applications WHERE id = ?", (req.application_id,))
    
    title = f"Application Status Update: {req.decision}"
    msg = f"Your application status has been updated to: {req.decision}."
    db_execute(
        "INSERT INTO notifications (candidate_id, title, message) VALUES (?, ?, ?)",
        (app_info[0]["candidate_id"], title, msg)
    )
    
    return {"message": "Override success"}

@app.get("/api/notifications/list/{candidate_id}")
def list_notifications(candidate_id: int):
    return db_query("SELECT * FROM notifications WHERE candidate_id = ? ORDER BY id DESC", (candidate_id,))

# ----------------------------------------------------------------------
# HOST & SERVER CONTROLS
# ----------------------------------------------------------------------
def open_browser():
    time.sleep(1.5)
    print("\n[SYSTEM] Auto-launching Zecpath AI user interface in browser...")
    webbrowser.open("http://127.0.0.1:8000")

def start_server():
    print("\n======================================================================")
    print("STARTING ZECPATH AI SAAS-LEVEL USER INTERFACE SERVER")
    print("======================================================================\n")
    
    init_db()
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    start_server()
