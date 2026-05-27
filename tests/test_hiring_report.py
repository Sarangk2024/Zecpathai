# tests/test_hiring_report.py

from ai_core.hiring_report_generator import generate_hiring_report, hiring_report_pipeline

def test_report():
    # Specifications-requested test structure
    result = generate_hiring_report("C1", 70, 70, 70, 70, 70, {
        "risk_level": "Low Risk",
        "integrity": "Low Risk"
    }, "Selected")
    assert "candidate_id" in result
    assert result["candidate_id"] == "C1"
    assert result["final_recommendation"] == "Selected"

def test_report_strengths_and_weaknesses():
    # Strong tech and ATS candidate
    result = generate_hiring_report(
        candidate_id="C9001",
        ats=85,
        screening=65,
        hr=80,
        technical=90,
        machine_test=60,
        behavior={
            "risk_level": "Moderate Risk",
            "integrity": "High Risk"
        },
        decision="Hold / Review"
    )
    
    assert "Strong resume-job match" in result["summary"]["strengths"]
    assert "Excellent technical skills" in result["summary"]["strengths"]
    assert "Screening responses need improvement" in result["summary"]["weaknesses"]
    assert "Weak real-world execution" in result["summary"]["weaknesses"]
    assert "Behavioral concerns detected" in result["summary"]["risks"]
    assert "Integrity risk detected" in result["summary"]["risks"]

def test_hiring_report_pipeline():
    data = {
        "candidate_id": "C999",
        "ats": 80,
        "screening": 80,
        "hr": 80,
        "technical": 80,
        "machine_test": 80,
        "behavior": {"risk_level": "Low Risk", "integrity": "Low Risk"},
        "decision": "Selected"
    }
    report = hiring_report_pipeline(data)
    assert len(report["summary"]["strengths"]) == 5
    assert len(report["summary"]["weaknesses"]) == 0
    assert len(report["summary"]["risks"]) == 0
