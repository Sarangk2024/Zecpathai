# tests/test_communication.py

from interview_ai.communication_engine import calculate_communication_score
from interview_ai.normalization import normalize_score

def test_communication():
    result = calculate_communication_score("I worked on projects")
    assert result["communication_score"] > 0

def test_excellent_communication():
    text = "I have experience in Python because I worked on backend systems. For example, I built several APIs."
    res = calculate_communication_score(text)
    assert res["communication_score"] >= 80.0
    assert res["breakdown"]["fluency"] == 1.0
    assert res["breakdown"]["grammar"] == 1.0
    assert res["breakdown"]["structure"] == 1.0
    assert res["breakdown"]["penalty"] == 0.0

def test_penalty_communication():
    text = "um like I actually don't know what basically to say here because um like yeah."
    res = calculate_communication_score(text)
    assert res["breakdown"]["penalty"] > 0.0

def test_normalization():
    assert normalize_score(50, 0, 100) == 50.0
    assert normalize_score(80, 50, 100) == 60.0
