# run_d28_report_generator.py - Standalone screening report generator runner (Day 28).

import json
from screening_ai.report_generator import generate_screening_report
from screening_ai.report_exporter import export_report_text

def main():
    print("\n==========================================================================================")
    print("ZECPATH AI SCREENING REPORT GENERATOR RUNNER (DAY 28)")
    print("==========================================================================================\n")

    # Mock Data matching Step 2 and 3 output definitions
    answers = [
        {
            "question_id": "Q1",
            "original_text": "I am a software developer with strong backend skills...",
            "skills": ["python", "django"],
            "availability": "Notice Period",
            "salary": "5 LPA"
        },
        {
            "question_id": "Q3",
            "original_text": "I have 2.5 years of experience working with Python and APIs...",
            "skills": ["python", "apis"],
            "experience_years": 2.5,
            "availability": "Notice Period",
            "salary": None
        }
    ]
    scores = [
        {"final_score": 82.0},
        {"final_score": 88.0}
    ]
    behavior_reports = [
        {"communication_strength": "Strong"},
        {"communication_strength": "Strong"}
    ]

    print("--- [STEP 1] COMPILING SCREENING REPORT ---")
    report = generate_screening_report("C789", "J202", answers, scores, behavior_reports)
    print("Recruiter-Ready Report Format JSON:")
    print(json.dumps(report, indent=2))

    print("\n--- [STEP 2] EXPORTING REPORT IN PLAIN TEXT FORMAT ---")
    exported_text = export_report_text(report)
    print(exported_text)

    print("\n------------------------------------------------------------------------------------------")
    print("Day 28 AI Screening Report Generator Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
