# run_d53_hiring_report.py

import json
from ai_core.hiring_report_generator import generate_hiring_report, hiring_report_pipeline

def main():
    print("\n==========================================================================================")
    print("ZECPATH HIRING INTELLIGENCE REPORT GENERATOR RUNNER (DAY 53)")
    print("==========================================================================================\n")

    # 1. Full Candidate AI Profile report
    print("--- [STEP 1] EXECUTING REPORT GENERATOR (FULL AI PROFILE) ---")
    data = {
        "candidate_id": "C12001",
        "ats": 78,
        "screening": 72,
        "hr": 80,
        "technical": 85,
        "machine_test": 76,
        "behavior": {
            "confidence": 82,
            "risk_level": "Low Risk",
            "integrity": "Moderate Risk"
        },
        "decision": "Selected"
    }
    
    report = hiring_report_pipeline(data)
    print("Full Candidate AI Profile JSON:")
    print(json.dumps(report, indent=2))

    # 2. Export-Ready JSON Format Layout
    print("\n--- [STEP 2] EXPORT-READY JSON LAYOUT ---")
    export_ready = {
        "candidate_id": report["candidate_id"],
        "final_score": 81.2, # unified score computed separately
        "decision": report["final_recommendation"],
        "report": report
    }
    print(json.dumps(export_ready, indent=2))

    # 3. Text Report (Recruiter View)
    print("\n--- [STEP 3] TEXT REPORT (RECRUITER VIEW) ---")
    text_view = f"""
    Candidate ID: {report["candidate_id"]}
    Overall Performance:
    - ATS Score: {report["scores"]["ats"]}
    - Screening Score: {report["scores"]["screening"]}
    - HR Score: {report["scores"]["hr"]}
    - Technical Score: {report["scores"]["technical"]}
    - Machine Test Score: {report["scores"]["machine_test"]}
    
    Strengths:
    """
    for s in report["summary"]["strengths"]:
        text_view += f"    + {s}\n"
        
    text_view += "    Weaknesses:\n"
    for w in report["summary"]["weaknesses"]:
        text_view += f"    - {w}\n"
        
    text_view += "    Risks:\n"
    for r in report["summary"]["risks"]:
        text_view += f"    [WARN] {r}\n"
        
    text_view += f"""    Final Recommendation: {report["final_recommendation"].upper()}
    Confidence Level: High
    """
    print(text_view)

    print("------------------------------------------------------------------------------------------")
    print("Day 53 Hiring Intelligence Report Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
