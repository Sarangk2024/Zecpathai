# api/integration_pipeline.py

def parse_resume(data):
    # Simulated parse
    return {
        "candidate_id": data.get("candidate_id", "C100"),
        "skills": ["Python", "Django"],
        "experience": 2
    }

def ats_score(resume):
    # Simulated ATS score
    return 78

def screening_ai(data):
    # Simulated screening score
    return 72

def interview_ai(data):
    # Simulated HR score
    return 80

def technical_ai(data):
    # Simulated technical score
    return 85

def decision_engine(scores):
    avg_score = sum(scores.values()) / len(scores) if scores else 0
    decision = "Selected" if avg_score >= 75 else "Rejected"
    return {
        "decision": decision,
        "confidence": 85
    }

def full_integration_pipeline(data):
    resume = parse_resume(data)
    ats = ats_score(resume)
    screening = screening_ai(data)
    hr = interview_ai(data)
    tech = technical_ai(data)
    
    final = decision_engine({
        "ats": ats,
        "screening": screening,
        "hr": hr,
        "technical": tech
    })
    return final
