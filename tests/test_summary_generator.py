# tests/test_summary_generator.py

from interview_ai.summary_generator import generate_interview_summary

def test_summary_generator():
    hr_scores = [
        {"question_id": "Q1", "final_score": 85.0},
        {"question_id": "Q2", "final_score": 90.0}
    ]
    communication = {
        "communication_score": 85.0
    }
    behavior = {
        "confidence": {"confidence_score": 80.0},
        "contradiction": False,
        "behavioral_score": 85.0
    }
    answers = ["I worked in a team environment to solve problems."]
    
    summary = generate_interview_summary(
        "C101",
        hr_scores,
        communication,
        behavior,
        answers
    )
    
    assert summary["candidate_id"] == "C101"
    assert summary["decision"] == "Strong Hire"
    assert "Strong performance in Q1" in summary["summary"]["strengths"]
    assert "Shows teamwork orientation" in summary["summary"]["strengths"]
    assert summary["summary"]["cultural_fit"] == "Good"
    assert "natural_language_summary" in summary
