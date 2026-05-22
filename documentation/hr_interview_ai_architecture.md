# Zecpath HR Interview AI – System Architecture

## High-Level Architecture
```
Frontend (Web / App)
        ↓
Backend API Layer
        ↓
-----------------------------------
      HR Interview AI System
-----------------------------------
1. Question Generator
2. Conversation Engine
3. Follow-Up Engine
4. Answer Understanding Engine
5. Communication Analyzer
6. Confidence & Behavior Analyzer
7. HR Scoring Engine
8. Aptitude Engine
9. Summary Generator
-----------------------------------
        ↓
Database / Storage
```

## Data Flow
```
User Input (Voice/Text)
        ↓
Speech-to-Text (STT)
        ↓
Answer Processing (Intent + Entity Cleanup)
        ↓
AI Evaluation (Scoring + Behavior + Confidence)
        ↓
Report Generation
        ↓
API Response → Frontend / Recruiter Dashboard
```

## Core Modules

| Module | Responsibility |
| --- | --- |
| **Question Engine** | Generates HR questions dynamically based on role type and experience |
| **Conversation Engine** | Manages interview state, session progression, and flow |
| **NLP Engine** | Understands verbal answers, extracts skills, and analyzes intent |
| **Scoring Engine** | Evaluates answers on Relevance, Communication, Confidence, and Consistency |
| **Behavior AI** | Detects confidence levels and identifies hesitation/stress patterns |
| **Report Generator** | Outputs summaries, lists candidate strengths, weaknesses, and final recommendations |
