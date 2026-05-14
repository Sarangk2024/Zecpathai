# tests/test_report_generator.py

from screening_ai.report_generator import generate_screening_report
from screening_ai.report_exporter import export_report_text

def test_report():
    report = generate_screening_report(
        "C1", "J1", [], [], []
    )
    assert "candidate_id" in report

def test_full_report_generation():
    answers = [
        {
            "question_id": "Q1",
            "original_text": "I am a developer.",
            "skills": ["python"],
            "availability": "Unknown"
        },
        {
            "question_id": "Q3",
            "original_text": "I have experience.",
            "skills": ["django"],
            "experience_years": 3,
            "availability": "Immediate"
        }
    ]
    scores = [
        {"final_score": 85.0},
        {"final_score": 90.0}
    ]
    behavior_reports = [
        {"communication_strength": "Strong"},
        {"communication_strength": "Strong"}
    ]
    
    report = generate_screening_report("C123", "J101", answers, scores, behavior_reports)
    assert report["candidate_id"] == "C123"
    assert report["final_score"] == 87.5
    assert report["decision"] == "Proceed"
    assert "Strong answer in Q1" in report["summary"]["strengths"]
    assert "Strong experience explanation" in report["summary"]["strengths"]
    assert "django" in report["highlights"]["confirmed_skills"]
    assert report["highlights"]["availability"] == "Immediate"
    
    text = export_report_text(report)
    assert "Candidate ID: C123" in text
    assert "Decision: Proceed" in text
