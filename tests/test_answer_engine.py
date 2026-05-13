# tests/test_answer_engine.py - Unit tests for Answer Intent and Extraction.

from screening_ai.answer_engine import process_answer, classify_intent

def test_answer_processing():
    text = "I have 2 years experience in Python"
    result = process_answer("Q3", text)
    assert result["intent"] == "experience"
    assert result["experience_years"] == 2
    assert "python" in result["skills"]

def test_salary_extraction():
    text = "Expecting around 5 LPA package."
    result = process_answer("Q6", text)
    assert result["intent"] == "salary"
    assert result["salary"] == "5 lpa"

def test_notice_period_extraction():
    text = "I have an immediate availability."
    result = process_answer("Q7", text)
    assert result["availability"] == "Immediate"

def test_vague_answers():
    text = "Maybe 3 years, not sure."
    result = process_answer("Q3", text)
    assert result["is_vague"] is True

def test_off_topic_detection():
    text = "I like playing soccer on weekends."
    result = process_answer("Q1", text)
    assert result["off_topic"] is True
