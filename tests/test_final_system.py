# tests/test_final_system.py

from interview_ai.final_hr_module import run_hr_interview

def test_final_system():
    # Specifications-requested test
    result = run_hr_interview("C1", [], {"communication_score": 70}, {
        "confidence": {"confidence_score": 70},
        "behavioral_score": 70,
        "contradiction": False
    })
    assert "final_score" in result

def test_final_system_with_answers():
    answers = [
        {
            "question_id": "Q1",
            "answer_text": "I am a backend developer with experience in Python and APIs.",
            "relevance_score": 0.8,
            "communication_score": 80,
            "confidence_score": 85,
            "contradiction": False,
            "is_vague": False
        },
        {
            "question_id": "Q2",
            "answer_text": "I worked with a team to deliver projects on time.",
            "relevance_score": 0.9,
            "communication_score": 85,
            "confidence_score": 80,
            "contradiction": False,
            "is_vague": False
        }
    ]
    communication = {"communication_score": 82}
    behavior = {
        "confidence": {"confidence_score": 82},
        "behavioral_score": 80,
        "contradiction": False
    }
    
    result = run_hr_interview("C1001", answers, communication, behavior)
    assert result["candidate_id"] == "C1001"
    assert result["final_score"] > 0
    assert "decision" in result
    assert "summary" in result
    assert result["summary"]["summary"]["cultural_fit"] == "Good"
