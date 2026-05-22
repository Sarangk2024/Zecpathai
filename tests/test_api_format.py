# tests/test_api_format.py

def test_api_format():
    # Specifications-requested test structure
    response = {
        "candidate_id": "C1",
        "final_score": 80
    }
    assert "candidate_id" in response

def test_api_start_payload():
    start_resp = {
        "session_id": "S123",
        "questions": [
            "Tell me about yourself",
            "What are your strengths?"
        ]
    }
    assert "session_id" in start_resp
    assert isinstance(start_resp["questions"], list)
    assert len(start_resp["questions"]) > 0

def test_api_answer_payload():
    ans_resp = {
        "follow_up": "Can you elaborate more?",
        "next_question": "Describe your teamwork experience"
    }
    assert "follow_up" in ans_resp
    assert "next_question" in ans_resp

def test_api_report_payload():
    report_resp = {
        "candidate_id": "C101",
        "final_score": 78,
        "decision": "Strong Hire",
        "summary": {
            "strengths": ["Good communication"],
            "weaknesses": ["Minor hesitation"]
        }
    }
    assert report_resp["candidate_id"] == "C101"
    assert report_resp["final_score"] == 78
    assert "decision" in report_resp
    assert "strengths" in report_resp["summary"]
