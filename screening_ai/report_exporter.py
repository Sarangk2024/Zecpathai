# screening_ai/report_exporter.py

def export_report_text(report):
    strengths = "\n".join(report['summary']['strengths'])
    risks = "\n".join(report['summary']['risks'])
    missing = "\n".join(report['summary']['missing_data'])
    skills_list = [str(s) for s in report['highlights']['confirmed_skills']]
    skills = ", ".join(skills_list)
    
    text = f"""
Candidate ID: {report['candidate_id']}
Job ID: {report['job_id']}
Final Score: {report['final_score']}
Decision: {report['decision']}
--- Strengths ---
{strengths}
--- Risks ---
{risks}
--- Missing Data ---
{missing}
--- Highlights ---
Salary: {report['highlights']['salary_expectation']}
Availability: {report['highlights']['availability']}
Skills: {skills}
"""
    return text.strip()
