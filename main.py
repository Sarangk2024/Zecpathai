# main.py - Main entry point to launch Zecpath AI web server / user interface.

import sys
import os
import webbrowser
import threading
import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

# Import core scoring logic directly
from ai_core.release_ready_system import release_pipeline

app = FastAPI(title="Zecpath AI Hiring Portal")

# Active log logs container
observability_logs = []

class CandidateSimulationPayload(BaseModel):
    candidate_id: str
    name: str
    ats_score: float
    screening_score: float
    hr_score: float
    technical_score: float
    machine_test_score: float
    behavior_risk: str
    integrity_risk: str

# HTML frontend code
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zecpath AI - Autonomous Hiring Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #070a13;
            --bg-panel: #0d1222;
            --bg-card: rgba(20, 27, 49, 0.6);
            --border-glow: rgba(99, 102, 241, 0.15);
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
            padding: 1.5rem 3rem;
            background-color: rgba(13, 18, 34, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo {
            font-size: 1.4rem;
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

        .tab-btn:hover:not(.active) {
            color: var(--text-main);
            background-color: rgba(255, 255, 255, 0.03);
        }

        .main-container {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Dashboard & Stepper Styles */
        .dashboard-layout {
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 2rem;
        }

        .control-panel {
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
            margin-bottom: 1rem;
        }

        .form-group label {
            display: block;
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 0.35rem;
            font-weight: 500;
        }

        .form-select, .form-input {
            width: 100%;
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #fff;
            padding: 0.6rem 0.8rem;
            border-radius: 6px;
            outline: none;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }

        .form-select:focus, .form-input:focus {
            border-color: var(--color-primary);
            box-shadow: 0 0 8px var(--border-glow);
        }

        .scores-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
        }

        .run-btn {
            width: 100%;
            background: linear-gradient(135deg, var(--color-primary), #8b5cf6);
            border: none;
            color: #fff;
            padding: 0.8rem;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 1.25rem;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            transition: all 0.2s ease;
        }

        .run-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        }

        .simulation-area {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        /* Stepper Pipeline */
        .stepper-container {
            background-color: var(--bg-panel);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .stepper {
            display: flex;
            justify-content: space-between;
            position: relative;
            margin: 1.5rem 0;
        }

        .stepper::before {
            content: '';
            position: absolute;
            top: 18px;
            left: 20px;
            right: 20px;
            height: 2px;
            background-color: rgba(255, 255, 255, 0.05);
            z-index: 1;
        }

        .step-progress-bar {
            position: absolute;
            top: 18px;
            left: 20px;
            height: 2px;
            width: 0%;
            background: linear-gradient(90deg, var(--color-primary), var(--color-success));
            z-index: 1;
            transition: width 0.4s ease;
        }

        .step {
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            z-index: 2;
            width: 80px;
        }

        .step-circle {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background-color: #111827;
            border: 2px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            transition: all 0.3s ease;
        }

        .step-title {
            font-size: 0.7rem;
            font-weight: 500;
            margin-top: 0.5rem;
            color: var(--text-muted);
            text-align: center;
            white-space: nowrap;
        }

        .step.active .step-circle {
            border-color: var(--color-primary);
            color: #fff;
            box-shadow: 0 0 12px var(--color-primary-glow);
            background-color: var(--bg-base);
            animation: pulse 1.5s infinite;
        }

        .step.active .step-title {
            color: #fff;
            font-weight: 600;
        }

        .step.completed .step-circle {
            border-color: var(--color-success);
            background-color: rgba(16, 185, 129, 0.1);
            color: var(--color-success);
        }

        .step.completed .step-title {
            color: var(--color-success);
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
            70% { box-shadow: 0 0 0 8px rgba(99, 102, 241, 0); }
            100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
        }

        /* Results Panel */
        .results-panel {
            background-color: var(--bg-panel);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            display: none;
        }

        .results-grid {
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 2rem;
            margin-top: 1rem;
        }

        .gauge-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            padding-right: 2rem;
        }

        .score-circle {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            background: radial-gradient(circle, var(--bg-panel) 55%, transparent 60%),
                        conic-gradient(var(--color-primary) 0%, rgba(255,255,255,0.05) 0%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        }

        .score-val {
            font-size: 2.2rem;
            font-weight: 700;
            color: #fff;
        }

        .score-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 0.15rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .decision-badge {
            margin-top: 1rem;
            padding: 0.35rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .badge-selected {
            background-color: rgba(16, 185, 129, 0.15);
            border: 1px solid var(--color-success);
            color: var(--color-success);
        }

        .badge-hold {
            background-color: rgba(245, 158, 11, 0.15);
            border: 1px solid var(--color-warning);
            color: var(--color-warning);
        }

        .badge-rejected {
            background-color: rgba(239, 68, 68, 0.15);
            border: 1px solid var(--color-danger);
            color: var(--color-danger);
        }

        .report-details {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .card-metrics {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 0.75rem;
        }

        .metric-card {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 0.75rem;
            border-radius: 8px;
            text-align: center;
        }

        .metric-card-title {
            font-size: 0.7rem;
            color: var(--text-muted);
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        .metric-card-val {
            font-size: 1.1rem;
            font-weight: 600;
            color: #fff;
        }

        .strengths-weaknesses {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        .sw-box {
            padding: 1rem;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.01);
            border: 1px solid rgba(255, 255, 255, 0.03);
        }

        .sw-box h4 {
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }

        .sw-box.strengths h4 { color: var(--color-success); }
        .sw-box.weaknesses h4 { color: var(--color-warning); }

        .sw-list {
            list-style: none;
            font-size: 0.8rem;
            color: var(--text-muted);
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }

        .sw-list li::before {
            content: '•';
            margin-right: 0.35rem;
        }

        .sw-box.strengths li::before { color: var(--color-success); }
        .sw-box.weaknesses li::before { color: var(--color-warning); }

        /* Logger console */
        .console-panel {
            background-color: #070911;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            font-family: 'JetBrains Mono', monospace;
        }

        .console-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 0.5rem;
            margin-bottom: 0.75rem;
        }

        .console-title {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .console-title::before {
            content: '';
            width: 8px;
            height: 8px;
            background-color: var(--color-success);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 6px var(--color-success);
        }

        .console-body {
            height: 180px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            font-size: 0.8rem;
            color: #a78bfa;
            scroll-behavior: smooth;
        }

        .log-row {
            line-height: 1.4;
        }

        .log-time {
            color: #5b21b6;
            margin-right: 0.5rem;
        }

        .log-info { color: #818cf8; }
        .log-success { color: var(--color-success); }
        .log-warn { color: var(--color-warning); }

        /* Tab 2: Observability Dashboard */
        .metrics-overview {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .metric-hero {
            background-color: var(--bg-panel);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            text-align: center;
        }

        .metric-hero-val {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #fff, var(--text-muted));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0.5rem 0;
        }

        .metric-hero-title {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .alerts-panel {
            background-color: var(--bg-panel);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .alert-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(239, 68, 68, 0.08);
            border: 1px solid rgba(239, 68, 68, 0.2);
            padding: 1rem;
            border-radius: 8px;
            color: #fca5a5;
            font-size: 0.9rem;
            margin-bottom: 0.75rem;
        }

        .alert-item::before {
            content: '⚠';
            margin-right: 0.5rem;
            font-size: 1.1rem;
        }

        /* Tab 3: Handbook markdown */
        .handbook-panel {
            background-color: var(--bg-panel);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 2.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            line-height: 1.6;
        }

        .handbook-panel h2 {
            font-size: 1.5rem;
            color: #fff;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 0.35rem;
        }

        .handbook-panel p {
            margin-bottom: 1rem;
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        .handbook-panel code {
            font-family: 'JetBrains Mono', monospace;
            background-color: rgba(255, 255, 255, 0.04);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-size: 0.85rem;
            color: #f472b6;
        }

        .handbook-panel pre {
            background-color: #070911;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            margin-bottom: 1.25rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .handbook-panel pre code {
            background-color: transparent;
            padding: 0;
            color: #a78bfa;
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">ZECPATH AI</div>
        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('simulation')">Pipeline Simulator</button>
            <button class="tab-btn" onclick="switchTab('observability')">Observability Center</button>
            <button class="tab-btn" onclick="switchTab('handbook')">Developer Manual</button>
        </div>
    </header>

    <main class="main-container">
        <!-- TAB 1: PIPELINE RUNNER -->
        <div id="simulation" class="tab-content active">
            <div class="dashboard-layout">
                <!-- Side Panel Control -->
                <aside class="control-panel">
                    <div class="section-title">
                        <span>Simulate Candidate</span>
                    </div>
                    
                    <div class="form-group">
                        <label for="profile-select">Predefined Profiles</label>
                        <select id="profile-select" class="form-select" onchange="loadPresetProfile()">
                            <option value="custom">Custom Input Candidate</option>
                            <option value="c001">Arjun Nair (Strong Candidate)</option>
                            <option value="c002">Rahul Kumar (Average Candidate)</option>
                            <option value="c003">Ankit Sharma (Weak Candidate)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="cand-name">Candidate Name</label>
                        <input type="text" id="cand-name" class="form-input" value="Custom Candidate">
                    </div>

                    <div class="scores-grid">
                        <div class="form-group">
                            <label for="score-ats">ATS Match (%)</label>
                            <input type="number" id="score-ats" class="form-input" value="80" min="0" max="120">
                        </div>
                        <div class="form-group">
                            <label for="score-screening">Screening AI (%)</label>
                            <input type="number" id="score-screening" class="form-input" value="75" min="0" max="100">
                        </div>
                    </div>

                    <div class="scores-grid">
                        <div class="form-group">
                            <label for="score-hr">HR Fit (%)</label>
                            <input type="number" id="score-hr" class="form-input" value="80" min="0" max="100">
                        </div>
                        <div class="form-group">
                            <label for="score-technical">Technical AI (%)</label>
                            <input type="number" id="score-technical" class="form-input" value="85" min="0" max="100">
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="score-machine">Machine Challenge Sandbox (%)</label>
                        <input type="number" id="score-machine" class="form-input" value="80" min="0" max="100">
                    </div>

                    <div class="scores-grid">
                        <div class="form-group">
                            <label for="risk-behavior">Behavior Risk</label>
                            <select id="risk-behavior" class="form-select">
                                <option value="Low Risk">Low Risk</option>
                                <option value="Moderate Risk">Moderate Risk</option>
                                <option value="High Risk">High Risk</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="risk-integrity">Integrity Risk</label>
                            <select id="risk-integrity" class="form-select">
                                <option value="Low Risk">Low Risk</option>
                                <option value="Moderate Risk">Moderate Risk</option>
                                <option value="High Risk">High Risk</option>
                            </select>
                        </div>
                    </div>

                    <button class="run-btn" onclick="startPipelineRun()">Launch Evaluation Pipeline</button>
                </aside>

                <!-- Stepper & Simulation Logs Area -->
                <section class="simulation-area">
                    <!-- Visual Stepper -->
                    <div class="stepper-container">
                        <div class="section-title">
                            <span>Evaluations Progression Pipeline</span>
                        </div>
                        <div class="stepper">
                            <div class="step-progress-bar" id="step-progress"></div>
                            
                            <div class="step" id="step-1">
                                <div class="step-circle">1</div>
                                <div class="step-title">Resume Parsing</div>
                            </div>
                            <div class="step" id="step-2">
                                <div class="step-circle">2</div>
                                <div class="step-title">ATS Filter</div>
                            </div>
                            <div class="step" id="step-3">
                                <div class="step-circle">3</div>
                                <div class="step-title">Screening AI</div>
                            </div>
                            <div class="step" id="step-4">
                                <div class="step-circle">4</div>
                                <div class="step-title">HR Interview</div>
                            </div>
                            <div class="step" id="step-5">
                                <div class="step-circle">5</div>
                                <div class="step-title">Technical Test</div>
                            </div>
                            <div class="step" id="step-6">
                                <div class="step-circle">6</div>
                                <div class="step-title">Decision Engine</div>
                            </div>
                        </div>
                    </div>

                    <!-- Logger console panel -->
                    <div class="console-panel">
                        <div class="console-header">
                            <div class="console-title">Live System Pipeline Logs Stream</div>
                            <span style="font-size: 0.7rem; color: var(--text-muted)">STDOUT</span>
                        </div>
                        <div class="console-body" id="console-logs">
                            <div class="log-row"><span class="log-time">[SYSTEM]</span> Ready to process candidate simulations. Select parameters and click Launch.</div>
                        </div>
                    </div>

                    <!-- Evaluation scorecard results panel -->
                    <div class="results-panel" id="results-panel">
                        <div class="section-title">
                            <span>Aggregated Hiring Report Output</span>
                        </div>
                        <div class="results-grid">
                            <!-- Circular Gauge -->
                            <div class="gauge-wrapper">
                                <div class="score-circle" id="score-gauge">
                                    <span class="score-val" id="score-output">0%</span>
                                    <span class="score-label">Final Score</span>
                                </div>
                                <div class="decision-badge" id="decision-badge">HOLD</div>
                            </div>
                            
                            <!-- Detailed Report values -->
                            <div class="report-details">
                                <div class="card-metrics">
                                    <div class="metric-card">
                                        <div class="metric-card-title">ATS Score</div>
                                        <div class="metric-card-val" id="res-ats">0%</div>
                                    </div>
                                    <div class="metric-card">
                                        <div class="metric-card-title">Screening</div>
                                        <div class="metric-card-val" id="res-screening">0%</div>
                                    </div>
                                    <div class="metric-card">
                                        <div class="metric-card-title">HR Fit</div>
                                        <div class="metric-card-val" id="res-hr">0%</div>
                                    </div>
                                    <div class="metric-card">
                                        <div class="metric-card-title">Technical</div>
                                        <div class="metric-card-val" id="res-tech">0%</div>
                                    </div>
                                    <div class="metric-card">
                                        <div class="metric-card-title">Sandbox</div>
                                        <div class="metric-card-val" id="res-machine">0%</div>
                                    </div>
                                </div>

                                <div class="strengths-weaknesses">
                                    <div class="sw-box strengths">
                                        <h4>Strengths Identifiers</h4>
                                        <ul class="sw-list" id="strengths-list">
                                            <li>Evaluating pipeline...</li>
                                        </ul>
                                    </div>
                                    <div class="sw-box weaknesses">
                                        <h4>Behavior & Integrity Risks</h4>
                                        <ul class="sw-list" id="risks-list">
                                            <li>Evaluating pipeline...</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>

        <!-- TAB 2: OBSERVABILITY DASHBOARD -->
        <div id="observability" class="tab-content">
            <div class="metrics-overview">
                <div class="metric-hero">
                    <div class="metric-hero-title">Avg Latency</div>
                    <div class="metric-hero-val" id="metric-latency">0.95s</div>
                </div>
                <div class="metric-hero">
                    <div class="metric-hero-title">Success Rate</div>
                    <div class="metric-hero-val" id="metric-success">98.5%</div>
                </div>
                <div class="metric-hero">
                    <div class="metric-hero-title">Alert Status</div>
                    <div class="metric-hero-val" id="metric-alert" style="color: var(--color-success)">NOMINAL</div>
                </div>
                <div class="metric-hero">
                    <div class="metric-hero-title">Evaluations Ingested</div>
                    <div class="metric-hero-val" id="metric-runs">0</div>
                </div>
            </div>

            <div class="alerts-panel">
                <div class="section-title">
                    <span>Active Observability Anomalies Logs</span>
                </div>
                <div id="active-alerts-container">
                    <div style="color: var(--text-muted); font-size: 0.9rem; text-align: center; padding: 2rem;">No active alert violations. System metrics nominal.</div>
                </div>
            </div>
        </div>

        <!-- TAB 3: DEVELOPER HANDBOOK -->
        <div id="handbook" class="tab-content">
            <article class="handbook-panel">
                <h2>Zecpath AI - Integration Framework Guide</h2>
                <p>Welcome to the developer manual. This system utilizes high-accuracy scoring models decoupled into dedicated pipeline stages.</p>
                
                <h2>API Operations Reference</h2>
                <pre><code>POST /api/simulate
Content-Type: application/json

{
  "candidate_id": "C001",
  "name": "Arjun Nair",
  "ats_score": 85,
  "screening_score": 80,
  "hr_score": 85,
  "technical_score": 88,
  "machine_test_score": 85,
  "behavior_risk": "Low Risk",
  "integrity_risk": "Low Risk"
}</code></pre>

                <h2>Pipeline Weight Calculations</h2>
                <p>Calculations are normalized and aggregated applying the core formula parameters:</p>
                <pre><code>Final Score = (ATS * 20%) + (Screening * 15%) + (HR * 20%) + (Technical * 25%) + (Machine sandbox * 20%)</code></pre>
                <p>Risk deductions: Behavior Risk Deducts up to 10 points. Cheating Integrity Risk Deducts up to 15 points.</p>
            </article>
        </div>
    </main>

    <script>
        const PRESETS = {
            c001: { name: "Arjun Nair", ats: 85, screening: 80, hr: 85, tech: 88, machine: 85, behavior: "Low Risk", integrity: "Low Risk" },
            c002: { name: "Rahul Kumar", ats: 65, screening: 68, hr: 70, tech: 70, machine: 65, behavior: "Moderate Risk", integrity: "Low Risk" },
            c003: { name: "Ankit Sharma", ats: 40, screening: 50, hr: 55, tech: 45, machine: 40, behavior: "High Risk", integrity: "Moderate Risk" }
        };

        let evaluationCounter = 0;

        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }

        function loadPresetProfile() {
            const presetVal = document.getElementById('profile-select').value;
            if (presetVal === 'custom') return;
            
            const preset = PRESETS[presetVal];
            document.getElementById('cand-name').value = preset.name;
            document.getElementById('score-ats').value = preset.ats;
            document.getElementById('score-screening').value = preset.screening;
            document.getElementById('score-hr').value = preset.hr;
            document.getElementById('score-technical').value = preset.tech;
            document.getElementById('score-machine').value = preset.machine;
            document.getElementById('risk-behavior').value = preset.behavior;
            document.getElementById('risk-integrity').value = preset.integrity;
        }

        function addLog(message, type = 'info') {
            const consoleBody = document.getElementById('console-logs');
            const row = document.createElement('div');
            row.className = 'log-row';
            
            const timeSpan = document.createElement('span');
            timeSpan.className = 'log-time';
            timeSpan.innerText = `[${new Date().toLocaleTimeString()}]`;
            
            const msgSpan = document.createElement('span');
            msgSpan.className = `log-${type}`;
            msgSpan.innerText = message;
            
            row.appendChild(timeSpan);
            row.appendChild(msgSpan);
            consoleBody.appendChild(row);
            consoleBody.scrollTop = consoleBody.scrollHeight;
        }

        async function startPipelineRun() {
            const name = document.getElementById('cand-name').value;
            const ats = parseFloat(document.getElementById('score-ats').value);
            const screening = parseFloat(document.getElementById('score-screening').value);
            const hr = parseFloat(document.getElementById('score-hr').value);
            const tech = parseFloat(document.getElementById('score-technical').value);
            const machine = parseFloat(document.getElementById('score-machine').value);
            const behavior = document.getElementById('risk-behavior').value;
            const integrity = document.getElementById('risk-integrity').value;

            // Reset UI States
            document.getElementById('results-panel').style.display = 'none';
            document.querySelectorAll('.step').forEach(s => s.className = 'step');
            document.getElementById('step-progress').style.width = '0%';
            
            // Stepper Progression Animation Simulation
            const steps = [
                { id: 1, delay: 600, log: "Parsing candidate application resume text...", type: 'info' },
                { id: 2, delay: 600, log: `Applying ATS job description keyword matching patterns: Score ${ats}%`, type: 'info' },
                { id: 3, delay: 600, log: `Parsing Screening intent and conversational transcripts: Score ${screening}%`, type: 'info' },
                { id: 4, delay: 600, log: `Analyzing voice stress markers and confidence patterns: Score ${hr}%`, type: 'info' },
                { id: 5, delay: 600, log: `Executing code correctness parser and test sandbox: Score ${tech}%`, type: 'info' },
                { id: 6, delay: 600, log: "Integrating score aggregates and checking behavioral risks parameters...", type: 'success' }
            ];

            for (let i = 0; i < steps.length; i++) {
                const step = steps[i];
                document.getElementById(`step-${step.id}`).classList.add('active');
                addLog(step.log, step.type);
                
                await new Promise(r => setTimeout(r, step.delay));
                
                document.getElementById(`step-${step.id}`).classList.remove('active');
                document.getElementById(`step-${step.id}`).classList.add('completed');
                document.getElementById('step-progress').style.width = `${((i + 1) / steps.length) * 100}%`;
            }

            // Hit backend API to run core evaluations logic
            addLog("Executing core decision pipeline algorithm...", "info");
            try {
                const response = await fetch('/api/simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        candidate_id: 'C_UI_' + Math.floor(Math.random() * 1000),
                        name, ats_score: ats, screening_score: screening,
                        hr_score: hr, technical_score: tech, machine_test_score: machine,
                        behavior_risk: behavior, integrity_risk: integrity
                    })
                });
                
                const result = await response.json();
                
                // Show outcomes
                displayResults(result);
                evaluationCounter++;
                updateObservabilityMetrics(result);
                addLog(`Hiring recommendation generated successfully: ${result.decision}`, "success");
            } catch (err) {
                addLog("API Simulation error encountered: " + err, "warn");
            }
        }

        function displayResults(data) {
            document.getElementById('results-panel').style.display = 'block';
            
            // final score and gauge
            const roundedScore = Math.round(data.final_score);
            document.getElementById('score-output').innerText = roundedScore + '%';
            document.getElementById('score-gauge').style.background = `radial-gradient(circle, var(--bg-panel) 55%, transparent 60%), conic-gradient(var(--color-primary) ${roundedScore}%, rgba(255,255,255,0.05) ${roundedScore}%)`;
            
            // decision badge
            const badge = document.getElementById('decision-badge');
            badge.innerText = data.decision;
            badge.className = 'decision-badge';
            if (data.decision === 'Selected') badge.classList.add('badge-selected');
            else if (data.decision === 'Hold / Review') badge.classList.add('badge-hold');
            else badge.classList.add('badge-rejected');

            // Metric Cards
            document.getElementById('res-ats').innerText = Math.round(data.scores.ats) + '%';
            document.getElementById('res-screening').innerText = Math.round(data.scores.screening) + '%';
            document.getElementById('res-hr').innerText = Math.round(data.scores.hr) + '%';
            document.getElementById('res-tech').innerText = Math.round(data.scores.technical) + '%';
            document.getElementById('res-machine').innerText = Math.round(data.scores.machine_test) + '%';

            // Strengths and risks
            const strengthsList = document.getElementById('strengths-list');
            const risksList = document.getElementById('risks-list');
            
            strengthsList.innerHTML = '';
            risksList.innerHTML = '';
            
            if (data.final_score >= 75) {
                strengthsList.innerHTML += '<li>Strong aggregate evaluations match rating</li>';
            }
            if (data.scores.technical >= 80) {
                strengthsList.innerHTML += '<li>Advanced technical sandboxing and core programming knowledge</li>';
            }
            if (data.scores.ats >= 80) {
                strengthsList.innerHTML += '<li>Strong alignment with requested Job Description parameters</li>';
            }
            if (strengthsList.innerHTML === '') {
                strengthsList.innerHTML = '<li>No significant score indicators to report</li>';
            }

            // Risks
            let hasRisks = false;
            if (document.getElementById('risk-behavior').value !== 'Low Risk') {
                risksList.innerHTML += `<li>Behavior Risk flagged: ${document.getElementById('risk-behavior').value}</li>`;
                hasRisks = true;
            }
            if (document.getElementById('risk-integrity').value !== 'Low Risk') {
                risksList.innerHTML += `<li>Integrity / Cheating risk flagged: ${document.getElementById('risk-integrity').value}</li>`;
                hasRisks = true;
            }
            if (data.final_score < 60) {
                risksList.innerHTML += '<li>Score total below baseline recruitment standards</li>';
                hasRisks = true;
            }
            if (!hasRisks) {
                risksList.innerHTML = '<li>No behavioral or integrity anomalies detected</li>';
            }
        }

        function updateObservabilityMetrics(result) {
            document.getElementById('metric-runs').innerText = evaluationCounter;
            
            // Check latency and active alerts
            const alertsContainer = document.getElementById('active-alerts-container');
            alertsContainer.innerHTML = '';
            
            let alerts = [];
            
            // Simulate random latency between 0.5s and 2.5s to test alerting triggers
            const simulatedLatency = (Math.random() * 2 + 0.5).toFixed(2);
            document.getElementById('metric-latency').innerText = simulatedLatency + 's';
            
            if (simulatedLatency > 2.0) {
                alerts.push("High Latency Warning: Pipeline processing time exceeded 2.0s");
            }
            
            if (result.final_score < 50.0) {
                alerts.push("Fail Rate Threshold Warning: Candidate score fell below minimum quality baseline");
            }
            
            const alertStatus = document.getElementById('metric-alert');
            if (alerts.length > 0) {
                alertStatus.innerText = "WARNING";
                alertStatus.style.color = "var(--color-danger)";
                
                alerts.forEach(a => {
                    const alertDiv = document.createElement('div');
                    alertDiv.className = 'alert-item';
                    alertDiv.innerText = a;
                    alertsContainer.appendChild(alertDiv);
                });
            } else {
                alertStatus.innerText = "NOMINAL";
                alertStatus.style.color = "var(--color-success)";
                alertsContainer.innerHTML = '<div style="color: var(--text-muted); font-size: 0.9rem; text-align: center; padding: 2rem;">No active alert violations. System metrics nominal.</div>';
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return INDEX_HTML

@app.post("/api/simulate")
def simulate_pipeline(cand: CandidateSimulationPayload):
    # Pass metrics directly into backend aggregator logic
    raw_scores = {
        "ats": cand.ats_score,
        "screening": cand.screening_score,
        "hr": cand.hr_score,
        "technical": cand.technical_score,
        "machine_test": cand.machine_test_score
    }
    
    # Process pipeline metrics
    res = release_pipeline(cand.candidate_id, raw_scores)
    
    # Apply deductions for Behavior & Integrity risk manually since it mirrors actual logic
    final_score = res["final_score"]
    
    if cand.behavior_risk == "Moderate Risk":
        final_score -= 10.0
    elif cand.behavior_risk == "High Risk":
        final_score -= 20.0
        
    if cand.integrity_risk == "Moderate Risk":
        final_score -= 15.0
    elif cand.integrity_risk == "High Risk":
        final_score -= 30.0
        
    final_score = max(0.0, min(100.0, final_score))
    
    # Formulate decision recommendations
    if final_score >= 80.0:
        decision = "Selected"
    elif final_score >= 60.0:
        decision = "Hold / Review"
    else:
        decision = "Rejected"
        
    # Return formatted JSON metrics
    return {
        "candidate_id": cand.candidate_id,
        "scores": {
            "ats": cand.ats_score,
            "screening": cand.screening_score,
            "hr": cand.hr_score,
            "technical": cand.technical_score,
            "machine_test": cand.machine_test_score
        },
        "final_score": round(final_score, 2),
        "decision": decision
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
