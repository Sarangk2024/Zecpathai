# interview_ai/summary_generator.py

def generate_natural_summary(strengths, weaknesses, risks, culture_fit, decision):
    strengths_text = ', '.join(strengths[:2]) if strengths else 'some strengths'
    weaknesses_text = ', '.join(weaknesses[:2]) if weaknesses else 'minor weaknesses'
    risks_text = ', '.join(risks) if risks else 'no major risks'
    
    return f"""
The candidate demonstrates {strengths_text}.
However, there are concerns such as {weaknesses_text}.
Risk factors include {risks_text}.
Cultural fit is assessed as {culture_fit}.
Final Recommendation: {decision}.
""".strip()

def generate_interview_summary(candidate_id, hr_scores, communication, behavior, answers):
    strengths = []
    weaknesses = []
    risks = []
    inconsistencies = []
    
    # -------------------------------
    # Analyze HR Scores
    # -------------------------------
    for item in hr_scores:
        if item["final_score"] >= 80:
            strengths.append(f"Strong performance in {item['question_id']}")
        elif item["final_score"] < 50:
            weaknesses.append(f"Weak response in {item['question_id']}")
            
    # -------------------------------
    # Communication Analysis
    # -------------------------------
    if communication["communication_score"] >= 80:
        strengths.append("Excellent communication skills")
    elif communication["communication_score"] < 50:
        weaknesses.append("Poor communication clarity")
        
    # -------------------------------
    # Behavior Analysis
    # -------------------------------
    if behavior["confidence"]["confidence_score"] < 60:
        risks.append("Low confidence detected")
    if behavior["contradiction"]:
        inconsistencies.append("Contradictory statements observed")
        
    # -------------------------------
    # Cultural Fit Indicators
    # -------------------------------
    culture_fit = "Good"
    if "team" in str(answers).lower():
        strengths.append("Shows teamwork orientation")
    else:
        culture_fit = "Moderate"
        
    # -------------------------------
    # Final Summary
    # -------------------------------
    avg_hr = (sum(x["final_score"] for x in hr_scores) / len(hr_scores)) if hr_scores else 0.0
    overall_score = (
        communication["communication_score"] * 0.3 +
        behavior["behavioral_score"] * 0.3 +
        avg_hr * 0.4
    )
    
    decision = (
        "Strong Hire" if overall_score >= 75 else
        "Consider" if overall_score >= 55 else
        "Reject"
    )
    
    return {
        "candidate_id": candidate_id,
        "overall_score": round(overall_score, 2),
        "decision": decision,
        "summary": {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "risks": risks,
            "inconsistencies": inconsistencies,
            "cultural_fit": culture_fit
        },
        "natural_language_summary": generate_natural_summary(
            strengths, weaknesses, risks, culture_fit, decision
        )
    }
