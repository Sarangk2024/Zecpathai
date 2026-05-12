# tests/test_stt_processor.py - Unit tests for STT cleaning processor.

from screening_ai.stt_processor import clean_transcript

def test_cleaning():
    text = "um i am a developer"
    result = clean_transcript(text)
    # Check that fillers are removed
    assert "um" not in result["clean_text"]
    # Check that it gets capitalized
    assert result["clean_text"].startswith("I")
    # Check overall result matches expectations
    assert result["clean_text"] == "I am a developer."

def test_punctuation_and_capitalization():
    text = "i worked at a factory"
    result = clean_transcript(text)
    assert result["clean_text"] == "I worked at a factory."

def test_silence_detection():
    text = "   "
    result = clean_transcript(text)
    assert result["status"] == "silence_detected"
    assert result["clean_text"] == ""

def test_interrupted_speech_cleaning():
    text = "Javaaaaa and Django----"
    result = clean_transcript(text)
    assert "Java" in result["clean_text"]
