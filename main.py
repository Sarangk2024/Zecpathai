# main.py - Main entry point to launch Zecpath AI web server / user interface.

import sys
import os
import webbrowser
import threading
import time
import re
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Zecpath AI - Autonomous Hiring Job Portal")

# Active log logs container
observability_logs = []

# Mock Job Configurations
JOB_ROLES = {
    "mern": {
        "title": "MERN Stack Developer",
        "skills": ["react", "node.js", "express", "mongodb", "javascript"],
        "budget_min": 80000,
        "budget_max": 120000,
        "assessment_type": "coding",
        "instructions": "Implement a JavaScript function to reverse a string. Example: reverse('hello') -> 'olleh'."
    },
    "sales": {
        "title": "Sales Executive",
        "skills": ["communication", "negotiation", "crm", "leads", "sales"],
        "budget_min": 50000,
        "budget_max": 75000,
        "assessment_type": "aptitude",
        "question": "Which strategy is best for handling a customer objection about price?",
        "options": [
            "A. Suggest discount instantly to close sales.",
            "B. Re-emphasize value and ROI matching business outcomes.",
            "C. Explain that pricing is fixed and cannot be changed.",
            "D. Recommend competitor alternatives."
        ],
        "correct": "B"
    },
    "uiux": {
        "title": "UI/UX Designer",
        "skills": ["figma", "wireframe", "prototype", "photoshop", "design"],
        "budget_min": 70000,
        "budget_max": 95000,
        "assessment_type": "design_quiz",
        "question": "What does usability heuristics rule 'Consistency and Standards' refer to?",
        "options": [
            "A. Using unique layouts on every page.",
            "B. Maintaining uniform platform controls and patterns.",
            "C. Selecting bright primary colors.",
            "D. Ensuring high security authentication."
        ],
        "correct": "B"
    }
}

class AssessmentPayload(BaseModel):
    role_key: str
    code_content: str = ""
    aptitude_answer: str = ""

class NegotiationPayload(BaseModel):
    role_key: str
    expected_salary: float
    counter_offer_count: int

# HTML layout definition
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zecpath AI - Autonomous Job Portal</title>
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
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 40%);
            min-height: 100vh;
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

        .nav-tabs {
            display: flex;
            gap: 0.5rem;
            background: rgba(255, 255, 255, 0.03);
            padding: 0.25rem;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 0.5rem 1.25rem;
            font-size: 0.9rem;
            font-weight: 500;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .tab-btn.active {
            background-color: rgba(99, 102, 241, 0.15);
            color: #fff;
            box-shadow: 0 0 10px var(--border-glow);
        }

        .main-container {
            max-width: 1300px;
            margin: 2rem auto;
            padding: 0 2rem;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Layout Grid */
        .portal-grid {
            display: grid;
            grid-template-columns: 380px 1fr;
            gap: 2rem;
        }

        .card-panel {
            background-color: var(--bg-panel);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            height: fit-content;
        }

        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1.25rem;
            color: #fff;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

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
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #fff;
            padding: 0.65rem 0.85rem;
            border-radius: 6px;
            outline: none;
            font-size: 0.9rem;
            font-family: inherit;
            transition: all 0.2s ease;
        }

        .form-textarea {
            resize: vertical;
            height: 100px;
        }

        .form-select:focus, .form-input:focus, .form-textarea:focus {
            border-color: var(--color-primary);
            box-shadow: 0 0 8px var(--border-glow);
        }

        .file-upload-wrapper {
            position: relative;
            border: 2px dashed rgba(255,255,255,0.1);
            padding: 1.5rem;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            background: rgba(255,255,255,0.01);
            transition: all 0.2s ease;
        }

        .file-upload-wrapper:hover {
            border-color: var(--color-primary);
            background: rgba(99, 102, 241, 0.02);
        }

        .file-input {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            cursor: pointer;
        }

        .file-name-label {
            margin-top: 0.5rem;
            font-size: 0.8rem;
            color: var(--color-success);
            display: none;
        }

        .btn-action {
            width: 100%;
            background: linear-gradient(135deg, var(--color-primary), #8b5cf6);
            border: none;
            color: #fff;
            padding: 0.8rem;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            transition: all 0.2s ease;
        }

        .btn-action:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        }

        /* Steps Stepper Panel */
        .workspace-area {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .stepper-row {
            display: flex;
            justify-content: space-between;
            position: relative;
            background-color: var(--bg-panel);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .step {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 90px;
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
            transition: all 0.3s ease;
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
            animation: pulse-step 1.5s infinite;
        }

        .step.active .step-label {
            color: #fff;
            font-weight: 600;
        }

        .step.completed .step-num {
            border-color: var(--color-success);
            background-color: rgba(16, 185, 129, 0.1);
            color: var(--color-success);
        }

        .step.completed .step-label {
            color: var(--color-success);
        }

        @keyframes pulse-step {
            0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
            70% { box-shadow: 0 0 0 6px rgba(99, 102, 241, 0); }
            100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
        }

        /* Ingest Workspace Panels */
        .workspace-panel {
            background-color: var(--bg-panel);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            display: none;
        }

        .workspace-panel.active {
            display: block;
        }

        /* ATS Dashboard */
        .ats-results {
            display: grid;
            grid-template-columns: 180px 1fr;
            gap: 2rem;
        }

        .circle-gauge {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            background: radial-gradient(circle, var(--bg-panel) 55%, transparent 60%),
                        conic-gradient(var(--color-primary) 0%, rgba(255,255,255,0.05) 0%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        }

        .skills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }

        .skill-badge {
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #a5b4fc;
            padding: 0.25rem 0.6rem;
            border-radius: 4px;
            font-size: 0.75rem;
        }

        /* Voice Call Interface */
        .call-card {
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 8px;
            background: rgba(0,0,0,0.2);
            padding: 1.5rem;
            margin-top: 1rem;
        }

        .call-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }

        .voice-wave {
            display: flex;
            gap: 3px;
            align-items: center;
            height: 20px;
        }

        .voice-bar {
            width: 3px;
            height: 10px;
            background-color: var(--color-success);
            border-radius: 3px;
            animation: bounce-bar 0.8s infinite ease-in-out alternate;
        }

        .voice-bar:nth-child(2) { animation-delay: 0.2s; height: 16px; }
        .voice-bar:nth-child(3) { animation-delay: 0.4s; height: 12px; }
        .voice-bar:nth-child(4) { animation-delay: 0.1s; height: 18px; }

        @keyframes bounce-bar {
            0% { transform: scaleY(0.4); }
            100% { transform: scaleY(1.2); }
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

        /* Coding Sandbox Editor */
        .editor-container {
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 8px;
            overflow: hidden;
            margin-top: 1rem;
            background-color: #070a13;
        }

        .editor-header {
            background: #0f172a;
            padding: 0.5rem 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--text-muted);
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .editor-textarea {
            width: 100%;
            height: 150px;
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
            border-top: 1px solid rgba(255,255,255,0.05);
            min-height: 40px;
        }

        /* Offer Letter display */
        .offer-letter-doc {
            background-color: #fff;
            color: #111827;
            padding: 3rem;
            border-radius: 8px;
            font-family: 'Georgia', serif;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            line-height: 1.6;
            position: relative;
        }

        .offer-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #6366f1;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }

        .offer-body {
            font-size: 0.9rem;
        }

        .offer-body p {
            margin-bottom: 1.25rem;
        }

        .signature-box {
            margin-top: 3rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }

        /* Recruiter Tab dashboard cards */
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
            font-weight: 500;
            background-color: rgba(255,255,255,0.01);
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">ZECPATH AI PORTAL</div>
        <div class="nav-tabs">
            <button class="tab-btn active" id="tab-apply" onclick="switchTab('apply')">Apply Job</button>
            <button class="tab-btn" id="tab-recruiter" onclick="switchTab('recruiter')">Recruiter Console</button>
        </div>
    </header>

    <main class="main-container">
        <!-- TAB 1: JOB PORTAL APPLICANT -->
        <div id="apply-tab" class="tab-content active">
            <div class="portal-grid">
                <!-- Left panel: Application Form -->
                <aside class="card-panel">
                    <div class="section-title">
                        <span>Candidate Application</span>
                    </div>
                    
                    <div class="form-group">
                        <label for="job-select">Select Job Role</label>
                        <select id="job-select" class="form-select" onchange="loadJobRequirement()">
                            <option value="mern">MERN Stack Developer (Technical)</option>
                            <option value="sales">Sales Executive (Non-Technical)</option>
                            <option value="uiux">UI/UX Designer (Creative)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Resume Upload (.PDF / .TXT)</label>
                        <div class="file-upload-wrapper">
                            <span id="file-upload-title" style="font-size: 0.85rem; color: var(--text-muted);">Choose resume file or click drag</span>
                            <input type="file" id="resume-file" class="file-input" onchange="handleFileSelected()">
                            <div class="file-name-label" id="file-name-label">File ready</div>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="preset-resume-select">Or Paste Resume Text / Choose Preset</label>
                        <select id="preset-resume-select" class="form-select" onchange="loadPresetResumeText()">
                            <option value="">-- Choose Preset Text --</option>
                            <option value="strong_mern">Arjun Nair (Strong MERN Profile)</option>
                            <option value="average_mern">Rahul Kumar (Average MERN Profile)</option>
                            <option value="sales_exec">Suresh Menan (Sales Executive Profile)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="resume-text">Resume Raw Content</label>
                        <textarea id="resume-text" class="form-textarea" placeholder="Paste resume skills and experience text blocks..."></textarea>
                    </div>

                    <button class="btn-action" onclick="submitApplication()">Submit Job Application</button>
                </aside>

                <!-- Right workspace: Pipeline Stepper -->
                <section class="workspace-area">
                    <div class="stepper-row">
                        <div class="step" id="step-1">
                            <div class="step-num">1</div>
                            <div class="step-label">ATS Check</div>
                        </div>
                        <div class="step" id="step-2">
                            <div class="step-num">2</div>
                            <div class="step-label">Voice Screening</div>
                        </div>
                        <div class="step" id="step-3">
                            <div class="step-num">3</div>
                            <div class="step-label">Skills Assessment</div>
                        </div>
                        <div class="step" id="step-4">
                            <div class="step-num">4</div>
                            <div class="step-label">HR Negotiation</div>
                        </div>
                        <div class="step" id="step-5">
                            <div class="step-num">5</div>
                            <div class="step-label">Offer Dispatch</div>
                        </div>
                    </div>

                    <!-- WORKSPACE 1: ATS SCORE RESULT -->
                    <div class="workspace-panel" id="panel-ats">
                        <div class="section-title">
                            <span>Stage 1: AI ATS Screening Analytics</span>
                        </div>
                        <div class="ats-results">
                            <div class="circle-gauge" id="ats-gauge">
                                <span style="font-size: 2rem; font-weight: 700;" id="ats-score-output">0%</span>
                                <span style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase;">ATS Score</span>
                            </div>
                            <div>
                                <h3 style="margin-bottom: 0.5rem;" id="ats-verdict">Evaluating Candidate Job Match...</h3>
                                <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">The system parsed candidate requirements against job specs.</p>
                                
                                <h4 style="font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted);">Extracted Skills</h4>
                                <div class="skills-container" id="ats-skills-badge">
                                    <!-- Badges -->
                                </div>
                                <button class="btn-action" id="btn-to-screening" style="margin-top: 1.5rem; width: auto; padding: 0.6rem 1.5rem; display: none;" onclick="goToVoiceScreening()">Proceed to Voice Screening Call</button>
                            </div>
                        </div>
                    </div>

                    <!-- WORKSPACE 2: VOICE SCREENING CALL -->
                    <div class="workspace-panel" id="panel-voice">
                        <div class="section-title">
                            <span>Stage 2: Outbound AI voice Screening Call</span>
                        </div>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">A natural sounding AI bot is conducting the call to verify details.</p>
                        
                        <div class="call-card">
                            <div class="call-header">
                                <div style="font-weight: 600;" id="call-status">Call Status: Connected</div>
                                <div class="voice-wave">
                                    <div class="voice-bar"></div>
                                    <div class="voice-bar"></div>
                                    <div class="voice-bar"></div>
                                    <div class="voice-bar"></div>
                                </div>
                            </div>
                            <div class="dialogue-stream" id="voice-stream">
                                <!-- Dialogues -->
                            </div>
                            
                            <!-- Voice Input Box -->
                            <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                                <input type="text" id="voice-input" class="form-input" placeholder="Speak/Type your answer here..." onkeypress="handleVoiceEnter(event)">
                                <button class="btn-action" style="width: 80px;" onclick="submitVoiceResponse()">Speak</button>
                            </div>
                        </div>
                    </div>

                    <!-- WORKSPACE 3: ASSESSMENT ROUND (Role Specific) -->
                    <div class="workspace-panel" id="panel-assessment">
                        <div class="section-title">
                            <span>Stage 3: Candidate Competency & Code Sandbox Assessment</span>
                        </div>
                        
                        <div id="assessment-container">
                            <!-- Injected by job applied role -->
                        </div>
                    </div>

                    <!-- WORKSPACE 4: SALARY NEGOTIATION -->
                    <div class="workspace-panel" id="panel-negotiation">
                        <div class="section-title">
                            <span>Stage 4: Autonomous HR interview & Salary Negotiation</span>
                        </div>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">HR Bot will align expectations with company budget models.</p>
                        
                        <div class="call-card">
                            <div class="dialogue-stream" id="negotiation-stream">
                                <!-- Dialogue counter offers -->
                            </div>
                            <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                                <input type="number" id="negotiation-input" class="form-input" placeholder="Enter expected annual salary in USD (e.g. 95000)">
                                <button class="btn-action" style="width: 140px;" onclick="submitNegotiationResponse()">Counter Offer</button>
                            </div>
                        </div>
                    </div>

                    <!-- WORKSPACE 5: FINAL OFFER LETTER -->
                    <div class="workspace-panel" id="panel-offer">
                        <div class="section-title">
                            <span>Stage 5: Automated Offer Letter dispatch</span>
                        </div>
                        
                        <div class="offer-letter-doc">
                            <div class="offer-header">
                                <div>
                                    <h2 style="color: #6366f1; font-weight: 700;">ZECPATH AI PORTAL</h2>
                                    <span style="font-size: 0.75rem; color: #6b7280; font-family: sans-serif;">HR DEPT - DECENTRALIZED RECRUITMENT</span>
                                </div>
                                <span style="font-size: 0.85rem; color: #4b5563; font-family: sans-serif;">OFFER CONFIRMED</span>
                            </div>
                            
                            <div class="offer-body">
                                <p><strong>Date:</strong> <span id="offer-date">July 14, 2026</span></p>
                                <p><strong>To,</strong> <br><span id="offer-name">John Doe</span></p>
                                
                                <p>We are delighted to offer you the position of <strong><span id="offer-role">MERN Developer</span></strong> at Zecpath. Based on your outstanding evaluation score matching our core hiring pipeline criteria, we are pleased to confirm the following terms of employment:</p>
                                
                                <p><strong>Base Compensation:</strong> $<span id="offer-salary">0.00</span> USD per annum.</p>
                                <p><strong>Joining Date:</strong> August 1st, 2026.</p>
                                <p><strong>Key Duties:</strong> Backend microservices engineering, system optimization models, and AI observability logic.</p>
                                
                                <p>Please confirm your acceptance of this automated offer by signing below.</p>
                            </div>
                            
                            <div class="signature-box">
                                <div>
                                    <div style="font-size: 0.8rem; font-weight: 600; color: #4b5563;">Hiring Authority</div>
                                    <div style="font-family: cursive; font-size: 1.2rem; color: #6366f1; margin: 0.35rem 0;">Zecpath HR Bot</div>
                                    <div style="border-top: 1px solid #d1d5db; width: 150px;"></div>
                                </div>
                                <div>
                                    <div style="font-size: 0.8rem; font-weight: 600; color: #4b5563;">Candidate Signature</div>
                                    <div style="font-family: cursive; font-size: 1.2rem; color: #4b5563; margin: 0.35rem 0; cursor: pointer;" onclick="signOfferLetter()">Click to E-Sign</div>
                                    <div style="border-top: 1px solid #d1d5db; width: 150px;" id="signature-line"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>

        <!-- TAB 2: RECRUITER CONSOLE -->
        <div id="recruiter-tab" class="tab-content">
            <div class="rec-metrics">
                <div class="rec-metric-card">
                    <div style="font-size: 0.8rem; color: var(--text-muted)">Evaluations Ingested</div>
                    <div class="rec-metric-val" id="rec-total-runs">0</div>
                </div>
                <div class="rec-metric-card">
                    <div style="font-size: 0.8rem; color: var(--text-muted)">Average ATS score</div>
                    <div class="rec-metric-val" id="rec-avg-ats">0%</div>
                </div>
                <div class="rec-metric-card">
                    <div style="font-size: 0.8rem; color: var(--text-muted)">Hiring Conversion Rate</div>
                    <div class="rec-metric-val">100%</div>
                </div>
            </div>

            <div class="card-panel">
                <div class="section-title">
                    <span>Recruiter Candidate Tracking Pipeline</span>
                </div>
                <table class="pipeline-table">
                    <thead>
                        <tr>
                            <th>Candidate ID</th>
                            <th>Job Applied</th>
                            <th>ATS Score</th>
                            <th>Screening</th>
                            <th>Decision Recommendation</th>
                            <th>Offer Dispatched</th>
                        </tr>
                    </thead>
                    <tbody id="recruiter-pipeline-rows">
                        <!-- Table Rows -->
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <script>
        const PRESET_RESUMES = {
            strong_mern: "Arjun Nair has over 3 years of experience as a MERN Stack Developer. Arjun is expert in building APIs using react, node.js, express, and mongodb database modeling. Skilled in Javascript coding and system optimizations.",
            average_mern: "Rahul Kumar has 2 years of software engineering experience. Skilled in html, css, flask, and basics of react and node.js. Familar with Javascript and databases.",
            sales_exec: "Suresh Menan is an experienced Sales Executive with 4 years in lead generation and negotiation. Suresh is skilled in cold calling, communication, and managing sales CRM workflows."
        };

        let currentRoleKey = 'mern';
        let currentCandidate = {
            id: '',
            name: '',
            ats_score: 0,
            skills: [],
            screening_questions_idx: 0,
            expected_salary: 0,
            negotiation_attempts: 0
        };

        let recruiterData = [];

        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            
            document.getElementById(`${tabId}-tab`).classList.add('active');
            document.getElementById(`tab-${tabId}`).classList.add('active');
        }

        function loadJobRequirement() {
            currentRoleKey = document.getElementById('job-select').value;
        }

        function handleFileSelected() {
            const fileInput = document.getElementById('resume-file');
            const fileLabel = document.getElementById('file-name-label');
            const fileTitle = document.getElementById('file-upload-title');
            
            if (fileInput.files.length > 0) {
                const file = fileInput.files[0];
                fileTitle.innerText = "Selected Resume File:";
                fileLabel.innerText = file.name;
                fileLabel.style.display = "block";
                
                // Simulate reading text from file
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('resume-text').value = e.target.result;
                };
                reader.readAsText(file);
            }
        }

        function loadPresetResumeText() {
            const key = document.getElementById('preset-resume-select').value;
            if (key) {
                document.getElementById('resume-text').value = PRESET_RESUMES[key];
            }
        }

        async function submitApplication() {
            const role = document.getElementById('job-select').value;
            const text = document.getElementById('resume-text').value;
            
            if (!text.trim()) {
                alert("Please upload a file or paste resume text!");
                return;
            }

            // Reset stepper and tabs
            document.querySelectorAll('.step').forEach(s => s.className = 'step');
            document.querySelectorAll('.workspace-panel').forEach(p => p.classList.remove('active'));

            document.getElementById('step-1').classList.add('active');
            document.getElementById('panel-ats').classList.add('active');

            try {
                // Submit application to parse
                const formData = new FormData();
                formData.append("role_key", role);
                formData.append("resume_text", text);
                
                const response = await fetch('/api/apply', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                
                currentCandidate.id = result.candidate_id;
                currentCandidate.name = result.name;
                currentCandidate.ats_score = result.ats_score;
                currentCandidate.skills = result.skills;
                currentCandidate.screening_questions_idx = 0;
                currentCandidate.negotiation_attempts = 0;
                
                // Update ATS Panel
                document.getElementById('ats-score-output').innerText = Math.round(result.ats_score) + '%';
                document.getElementById('ats-gauge').style.background = `radial-gradient(circle, var(--bg-panel) 55%, transparent 60%), conic-gradient(var(--color-primary) ${result.ats_score}%, rgba(255,255,255,0.05) ${result.ats_score}%)`;
                
                const verdict = document.getElementById('ats-verdict');
                const btnScreening = document.getElementById('btn-to-screening');
                const skillsBadge = document.getElementById('ats-skills-badge');
                
                skillsBadge.innerHTML = '';
                result.skills.forEach(s => {
                    skillsBadge.innerHTML += `<span class="skill-badge">${s}</span>`;
                });

                if (result.ats_score >= 60) {
                    verdict.innerText = "Congratulations! ATS Shortlisted Successfully";
                    verdict.style.color = "var(--color-success)";
                    btnScreening.style.display = "inline-block";
                    document.getElementById('step-1').className = 'step completed';
                } else {
                    verdict.innerText = "Application Rejected: Score below hiring threshold.";
                    verdict.style.color = "var(--color-danger)";
                    btnScreening.style.display = "none";
                }
            } catch (err) {
                alert("ATS Error: " + err);
            }
        }

        // STAGE 2: VOICE SCREENING
        function goToVoiceScreening() {
            document.getElementById('panel-ats').classList.remove('active');
            document.getElementById('panel-voice').classList.add('active');
            document.getElementById('step-2').classList.add('active');
            
            // Start voice bot question loop
            const stream = document.getElementById('voice-stream');
            stream.innerHTML = '';
            
            const intro = `Hello ${currentCandidate.name}. I am the Zecpath AI voice screening bot. Let's start. Please introduce yourself and highlight your experience.`;
            appendBubble(intro, 'ai');
        }

        function appendBubble(text, speaker) {
            const stream = document.getElementById('voice-stream');
            const bubble = document.createElement('div');
            bubble.className = `bubble ${speaker}`;
            bubble.innerText = text;
            stream.appendChild(bubble);
            stream.scrollTop = stream.scrollHeight;
        }

        const SCREENING_QUESTIONS = [
            "What is your expected salary per annum in USD?",
            "What is your current location and notice period?"
        ];

        function handleVoiceEnter(event) {
            if (event.key === 'Enter') {
                submitVoiceResponse();
            }
        }

        function submitVoiceResponse() {
            const input = document.getElementById('voice-input');
            const text = input.value.trim();
            if (!text) return;
            
            appendBubble(text, 'user');
            input.value = '';
            
            // Check expected salary extraction from user chat bubble
            if (currentCandidate.screening_questions_idx === 0) {
                const match = text.match(/\\d+/);
                if (match) {
                    currentCandidate.expected_salary = parseFloat(match[0]);
                } else {
                    currentCandidate.expected_salary = 90000; # default counter
                }
            }

            setTimeout(() => {
                if (currentCandidate.screening_questions_idx < SCREENING_QUESTIONS.length) {
                    const nextQ = SCREENING_QUESTIONS[currentCandidate.screening_questions_idx];
                    appendBubble(nextQ, 'ai');
                    currentCandidate.screening_questions_idx++;
                } else {
                    appendBubble("Thank you! Voice screening completed. We are loading your round 3 competency assessment...", 'ai');
                    document.getElementById('step-2').className = 'step completed';
                    
                    setTimeout(() => {
                        loadAssessmentStage();
                    }, 1500);
                }
            }, 1000);
        }

        // STAGE 3: SKILLS ASSESSMENT
        function loadAssessmentStage() {
            document.getElementById('panel-voice').classList.remove('active');
            document.getElementById('panel-assessment').classList.add('active');
            document.getElementById('step-3').classList.add('active');
            
            const container = document.getElementById('assessment-container');
            container.innerHTML = '';
            
            if (currentRoleKey === 'mern') {
                container.innerHTML = `
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">Complete the programming challenge in the JavaScript sandbox:</p>
                    <div class="editor-container">
                        <div class="editor-header">
                            <span>Javascript sandbox editor (isPalindrome)</span>
                            <span>main.js</span>
                        </div>
                        <textarea class="editor-textarea" id="editor-code">function isPalindrome(str) {\\n  // Write code here\\n  return str.split('').reverse().join('') === str;\\n}</textarea>
                        <div class="editor-terminal" id="terminal-out">Terminal: Ready to run tests.</div>
                    </div>
                    <button class="btn-action" style="margin-top: 1rem;" onclick="submitAssessment()">Submit & Compile Code</button>
                `;
            } else if (currentRoleKey === 'sales') {
                container.innerHTML = `
                    <p style="font-size: 0.9rem; margin-bottom: 1rem;">Answer the business scenario multiple-choice question:</p>
                    <div class="form-group">
                        <p style="font-size: 0.85rem; font-weight: 500; margin-bottom: 0.75rem;">Which strategy is best for handling a customer objection about price?</p>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            <label><input type="radio" name="aptitude" value="A"> A. Suggest discount instantly to close sales.</label>
                            <label><input type="radio" name="aptitude" value="B"> B. Re-emphasize value and ROI matching business outcomes.</label>
                            <label><input type="radio" name="aptitude" value="C"> C. Explain that pricing is fixed and cannot be changed.</label>
                            <label><input type="radio" name="aptitude" value="D"> D. Recommend competitor alternatives.</label>
                        </div>
                    </div>
                    <button class="btn-action" onclick="submitAssessment()">Submit Answer</button>
                `;
            } else {
                container.innerHTML = `
                    <p style="font-size: 0.9rem; margin-bottom: 1rem;">Design theory assessment question:</p>
                    <div class="form-group">
                        <p style="font-size: 0.85rem; font-weight: 500; margin-bottom: 0.75rem;">What does usability heuristics rule 'Consistency and Standards' refer to?</p>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            <label><input type="radio" name="design" value="A"> A. Using unique layouts on every page.</label>
                            <label><input type="radio" name="design" value="B"> B. Maintaining uniform platform controls and patterns.</label>
                            <label><input type="radio" name="design" value="C"> C. Selecting bright primary colors.</label>
                            <label><input type="radio" name="design" value="D"> D. Ensuring high security authentication.</label>
                        </div>
                    </div>
                    <button class="btn-action" onclick="submitAssessment()">Submit Answer</button>
                `;
            }
        }

        async function submitAssessment() {
            let code = "";
            let choice = "";
            
            if (currentRoleKey === 'mern') {
                code = document.getElementById('editor-code').value;
                const term = document.getElementById('terminal-out');
                term.innerText = "Compiling JavaScript in sandbox environment...";
            } else {
                const name = currentRoleKey === 'sales' ? 'aptitude' : 'design';
                const checked = document.querySelector(`input[name="${name}"]:checked`);
                if (!checked) {
                    alert("Please select an answer!");
                    return;
                }
                choice = checked.value;
            }

            try {
                const response = await fetch('/api/assessment/evaluate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        role_key: currentRoleKey,
                        code_content: code,
                        aptitude_answer: choice
                    })
                });
                const result = await response.json();
                
                if (currentRoleKey === 'mern') {
                    const term = document.getElementById('terminal-out');
                    term.innerText = "Compilation details: " + result.message + " | Sandbox Score: " + result.score + "%";
                }

                currentCandidate.assessment_score = result.score;
                document.getElementById('step-3').className = 'step completed';

                setTimeout(() => {
                    loadNegotiationStage();
                }, 1500);
            } catch (err) {
                alert("Assessment error: " + err);
            }
        }

        // STAGE 4: NEGOTIATION
        function loadNegotiationStage() {
            document.getElementById('panel-assessment').classList.remove('active');
            document.getElementById('panel-negotiation').classList.add('active');
            document.getElementById('step-4').classList.add('active');
            
            const stream = document.getElementById('negotiation-stream');
            stream.innerHTML = '';
            
            const intro = `Based on your evaluation scores, you are qualified for employment. Your requested expected salary is $${currentCandidate.expected_salary} USD. Let's finalize contract expectations.`;
            appendNegotiationBubble(intro, 'ai');
        }

        function appendNegotiationBubble(text, speaker) {
            const stream = document.getElementById('negotiation-stream');
            const bubble = document.createElement('div');
            bubble.className = `bubble ${speaker}`;
            bubble.innerText = text;
            stream.appendChild(bubble);
            stream.scrollTop = stream.scrollHeight;
        }

        async function submitNegotiationResponse() {
            const input = document.getElementById('negotiation-input');
            const val = parseFloat(input.value);
            if (isNaN(val) || val <= 0) {
                alert("Please enter a valid salary counter offer!");
                return;
            }

            appendNegotiationBubble(`My counter offer: $${val} USD`, 'user');
            currentCandidate.expected_salary = val;
            currentCandidate.negotiation_attempts++;

            try {
                const response = await fetch('/api/negotiate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        role_key: currentRoleKey,
                        expected_salary: val,
                        counter_offer_count: currentCandidate.negotiation_attempts
                    })
                });
                const result = await response.json();

                setTimeout(() => {
                    appendNegotiationBubble(result.message, 'ai');
                    if (result.status === 'agreed') {
                        currentCandidate.final_salary = result.salary;
                        document.getElementById('step-4').className = 'step completed';
                        
                        setTimeout(() => {
                            loadOfferStage();
                        }, 1500);
                    }
                }, 1000);
            } catch (err) {
                alert("Negotiation error: " + err);
            }
        }

        // STAGE 5: OFFER LETTER
        async function loadOfferStage() {
            document.getElementById('panel-negotiation').classList.remove('active');
            document.getElementById('panel-offer').classList.add('active');
            document.getElementById('step-5').classList.add('active');
            
            // Set offer letters details
            document.getElementById('offer-name').innerText = currentCandidate.name;
            document.getElementById('offer-role').innerText = document.getElementById('job-select').options[document.getElementById('job-select').selectedIndex].text;
            document.getElementById('offer-salary').innerText = currentCandidate.final_salary.toLocaleString();
            
            // Ingest candidate log to Recruiter tracking metrics
            const finalScore = (currentCandidate.ats_score + currentCandidate.assessment_score) / 2;
            const payload = {
                id: currentCandidate.id,
                role: currentCandidate.name,
                ats: currentCandidate.ats_score,
                screening: finalScore,
                decision: finalScore >= 80 ? "Selected" : "Hold / Review",
                offer: "Dispatched"
            };
            recruiterData.push(payload);
            updateRecruiterConsole();
        }

        function signOfferLetter() {
            const signatureLine = document.getElementById('signature-line');
            signatureLine.innerHTML = `<span style="font-family: cursive; font-size: 1.2rem; color: #10b981;">${currentCandidate.name}</span>`;
            document.getElementById('step-5').className = 'step completed';
            alert("E-Signature Confirmed! Application pipeline fully completed!");
        }

        function updateRecruiterConsole() {
            document.getElementById('rec-total-runs').innerText = recruiterData.length;
            
            const totalAts = recruiterData.reduce((acc, c) => acc + c.ats, 0);
            const avgAts = recruiterData.length > 0 ? Math.round(totalAts / recruiterData.length) : 0;
            document.getElementById('rec-avg-ats').innerText = avgAts + '%';

            const tbody = document.getElementById('recruiter-pipeline-rows');
            tbody.innerHTML = '';
            recruiterData.forEach(c => {
                tbody.innerHTML += `
                    <tr>
                        <td><strong>${c.id}</strong></td>
                        <td>${c.role}</td>
                        <td>${Math.round(c.ats)}%</td>
                        <td>${Math.round(c.screening)}%</td>
                        <td><span class="decision-badge badge-selected">${c.decision}</span></td>
                        <td><span style="color: var(--color-success)">${c.offer}</span></td>
                    </tr>
                `;
            });
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return INDEX_HTML

@app.post("/api/apply")
def apply_resume(role_key: str = Form(...), resume_text: str = Form(...)):
    # Simulates parsing candidate name and calculating job-specific ATS scores
    name_match = re.search(r"([A-Z][a-z]+ [A-Z][a-z]+)", resume_text)
    candidate_name = name_match.group(1) if name_match else "Guest Applicant"
    
    # Matching keywords
    role_info = JOB_ROLES.get(role_key, JOB_ROLES["mern"])
    skills_matched = []
    
    for s in role_info["skills"]:
        if s in resume_text.lower():
            skills_matched.append(s.capitalize())
            
    # Score metrics
    matched_count = len(skills_matched)
    total_count = len(role_info["skills"])
    ats_score = round((matched_count / total_count) * 100.0, 2) if total_count > 0 else 50.0
    
    # Standard fallback
    if ats_score < 40.0:
        ats_score = 45.0 # fallback basic
        
    return {
        "candidate_id": f"C{int(time.time()) % 10000:04d}",
        "name": candidate_name,
        "ats_score": ats_score,
        "skills": skills_matched
    }

@app.post("/api/assessment/evaluate")
def evaluate_assessment(payload: AssessmentPayload):
    role = payload.role_key
    role_info = JOB_ROLES.get(role, JOB_ROLES["mern"])
    
    if role_info["assessment_type"] == "coding":
        # Simulate simple sandbox JavaScript correctness compiler checks
        code = payload.code_content
        if "reverse" in code and ("split" in code or "for" in code):
            score = 100.0
            msg = "Sandbox test cases passed. Function reverse() works."
        else:
            score = 50.0
            msg = "Sandbox syntax error or logic output failed."
    else:
        # Aptitude answer evaluations
        answer = payload.aptitude_answer
        correct_answer = role_info.get("correct", "B")
        if answer.strip().upper() == correct_answer:
            score = 100.0
            msg = "Correct answer selected."
        else:
            score = 0.0
            msg = "Incorrect answer selected."
            
    return {
        "score": score,
        "message": msg
    }

@app.post("/api/negotiate")
def negotiate_salary(payload: NegotiationPayload):
    role = payload.role_key
    role_info = JOB_ROLES.get(role, JOB_ROLES["mern"])
    
    min_budget = role_info["budget_min"]
    max_budget = role_info["budget_max"]
    expected = payload.expected_salary
    
    if expected <= max_budget:
        # Agreed salary
        agreed_salary = expected
        return {
            "status": "agreed",
            "salary": agreed_salary,
            "message": f"Perfect. We agree to your counter offer of ${agreed_salary:,} USD per annum."
        }
    else:
        # Counter offer logic
        if payload.counter_offer_count >= 3:
            # force agree at max budget
            return {
                "status": "agreed",
                "salary": max_budget,
                "message": f"To proceed with selection, we have set the contract cap at our maximum role budget of ${max_budget:,} USD."
            }
        else:
            # suggest halfway counter
            midpoint = (expected + max_budget) / 2
            counter_suggestion = round(midpoint)
            return {
                "status": "counter",
                "salary": counter_suggestion,
                "message": f"That is slightly above our budget limit. Can we align at a midpoint of ${counter_suggestion:,} USD per annum?"
            }

def open_browser():
    # Delay to let uvicorn startup server
    time.sleep(1.5)
    print("\n[SYSTEM] Auto-launching Zecpath AI user interface in browser...")
    webbrowser.open("http://127.0.0.1:8000")

def start_server():
    print("\n======================================================================")
    print("STARTING ZECPATH AI SAAS-LEVEL USER INTERFACE SERVER")
    print("======================================================================\n")
    
    # Start browser loader in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run FastAPI app
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    start_server()
