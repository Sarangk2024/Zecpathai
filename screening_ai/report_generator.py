# screening_ai/report_generator.py

def generate_screening_report(candidate_id, job_id, answers, scores, behavior_reports):
    strengths = []
    risks = []
    missing = []
    key_answers = []
    salary = None
    availability = None
    confirmed_skills = set()
    
    for ans, score, behavior in zip(answers, scores, behavior_reports):
        # Key Answers Summary
        key_answers.append({
            "question_id": ans["question_id"],
            "answer": ans["original_text"]
        })
        
        # Strengths
        if score["final_score"] >= 80:
            strengths.append(f"Strong answer in {ans['question_id']}")
            if ans["question_id"] == "Q3":
                strengths.append("Strong experience explanation")
                
        # Risks
        if score["final_score"] < 50 or behavior["communication_strength"] == "Weak":
            risks.append(f"Weak response in {ans['question_id']}")
            if ans["question_id"] == "Q6":
                risks.append("Weak clarity in salary discussion")
                
        # Missing Data
        if ans.get("is_vague") or ans.get("off_topic"):
            missing.append(f"Incomplete answer in {ans['question_id']}")
            
        # Extract highlights
        if ans.get("salary"):
            salary = ans["salary"]
        if ans.get("availability") != "Unknown" and ans.get("availability") is not None:
            availability = ans["availability"]
        for skill in ans.get("skills", []):
            confirmed_skills.add(skill)
            
    final_score = sum(s["final_score"] for s in scores) / len(scores) if scores else 0
    decision = "Proceed" if final_score >= 70 else "Review" if final_score >= 50 else "Reject"
    
    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "final_score": round(final_score, 2),
        "decision": decision,
        "summary": {
            "strengths": strengths,
            "risks": risks,
            "missing_data": missing
        },
        "highlights": {
            "salary_expectation": salary,
            "availability": availability,
            "confirmed_skills": list(confirmed_skills)
        },
        "answers": key_answers
    }
