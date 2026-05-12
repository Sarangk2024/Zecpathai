# tests/test_transcript.py - Unit tests for transcript normalizer.

from screening_ai.transcript_normalizer import normalize_transcript, process_transcript

def test_normalization():
    text = "Um I have like 3 years experience"
    result = normalize_transcript(text)
    assert "um" not in result
    assert "like" not in result
    assert result == "i have 3 years experience"

def test_normalization_casing_and_spaces():
    text = "   Uh I worked   at  Wipro   "
    result = normalize_transcript(text)
    assert "uh" not in result
    assert result == "i worked at wipro"

def test_process_transcript():
    raw_answers = [
        {"question_id": "Q1", "text": "Um, I am Sarang.", "confidence": 0.95},
        {"question_id": "Q3", "text": "I have like 4 years experience.", "confidence": 0.88}
    ]
    processed = process_transcript(raw_answers)
    assert len(processed) == 2
    assert processed[0]["answer_text"] == ", i am sarang."  # basic string cleaning
    assert "like" not in processed[1]["answer_text"]
    assert processed[0]["confidence_score"] == 0.95
