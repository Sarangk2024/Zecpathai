# ai_core/hiring_report_generator.py

def generate_hiring_report(candidate_id, ats, screening, hr, technical, machine_test, behavior, decision):
    # -------------------------------
    # Strengths & Weaknesses
    # -------------------------------
    strengths = []
    weaknesses = []
    risks = []
    
    if ats >= 75:
        strengths.append("Strong resume-job match")
    else:
        weaknesses.append("Weak resume alignment")
        
    if screening >= 70:
        strengths.append("Good screening performance")
    else:
        weaknesses.append("Screening responses need improvement")
        
    if hr >= 75:
        strengths.append("Strong HR interview performance")
    else:
        weaknesses.append("HR responses lacked depth")
        
    if technical >= 80:
        strengths.append("Excellent technical skills")
    else:
        weaknesses.append("Technical depth needs improvement")
        
    if machine_test >= 75:
        strengths.append("Good practical coding ability")
    else:
        weaknesses.append("Weak real-world execution")
        
    if behavior.get("risk_level") != "Low Risk":
        risks.append("Behavioral concerns detected")
    if behavior.get("integrity") != "Low Risk":
        risks.append("Integrity risk detected")
        
    # -------------------------------
    # Final Report Object
    # -------------------------------
    return {
        "candidate_id": candidate_id,
        "scores": {
            "ats": ats,
            "screening": screening,
            "hr": hr,
            "technical": technical,
            "machine_test": machine_test
        },
        "behavior": behavior,
        "summary": {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "risks": risks
        },
        "final_recommendation": decision
    }

def hiring_report_pipeline(data):
    report = generate_hiring_report(
        data["candidate_id"],
        data["ats"],
        data["screening"],
        data["hr"],
        data["technical"],
        data["machine_test"],
        data["behavior"],
        data["decision"]
    )
    return report
