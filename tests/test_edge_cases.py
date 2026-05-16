# tests/test_edge_cases.py

from screening_ai.robust_flow import detect_edge_case, handle_edge_case
from screening_ai.error_framework import get_error_response, fallback_strategy
from screening_ai.noise_handler import clean_noise, detect_language_mix

def test_missing():
    result = detect_edge_case("", 1.0)
    assert result == "missing"

def test_poor_audio():
    result = detect_edge_case("hello", 0.4)
    assert result == "poor_audio"

def test_language_mix():
    assert detect_edge_case("chetta enna hai", 1.0) == "language_mix"
    assert detect_language_mix("chetta enna hai") is True
    assert detect_language_mix("regular english answer") is False

def test_noise_clean():
    assert clean_noise("hello [background cough] world") == "hello  world"
    assert clean_noise("Javaaaaa and Django----") == "Java and Django-"

def test_handle_edge_case():
    assert handle_edge_case(None, "", 1.0, 0) == "retry"
    assert handle_edge_case(None, "hi", 0.3, 0) == "ask_repeat_audio"
    assert handle_edge_case(None, "um", 1.0, 0) == "simplify_question"
    assert handle_edge_case(None, "hi chetta", 1.0, 0) == "switch_language"
    assert handle_edge_case(None, "hi", 1.0, 0) == "ask_detail"
    assert handle_edge_case(None, "I am a developer", 1.0, 0) == "next"

def test_error_and_fallbacks():
    assert get_error_response("missing") == "I didn’t receive your response. Could you please answer?"
    assert get_error_response("unknown") == "Let’s move to the next question."
    assert fallback_strategy("missing", 0) == "retry"
    assert fallback_strategy("missing", 2) == "skip_question"
    assert fallback_strategy("language_mix", 0) == "switch_language"
