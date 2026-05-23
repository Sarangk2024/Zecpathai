# tests/test_technical_design.py

from technical_ai.experience_logic import get_experience_level
from technical_ai.difficulty_engine import adjust_difficulty
from technical_ai.question_generator import generate_question

def test_experience():
    # Specifications-requested test
    assert get_experience_level(3) == "3-5"
    assert get_experience_level(1) == "0-2"
    assert get_experience_level(6) == "5+"

def test_adjust_difficulty():
    assert adjust_difficulty("basic", "good") == "intermediate"
    assert adjust_difficulty("intermediate", "good") == "advanced"
    assert adjust_difficulty("advanced", "good") == "advanced"
    assert adjust_difficulty("advanced", "poor") == "intermediate"
    assert adjust_difficulty("intermediate", "poor") == "basic"
    assert adjust_difficulty("basic", "poor") == "basic"

def test_question_generator():
    js_basic = generate_question("JavaScript", "basic")
    assert js_basic in ["What is a variable?", "Explain let vs var"]
    
    python_advanced = generate_question("Python", "advanced")
    assert python_advanced == "Design scalable backend system"
    
    unknown = generate_question("Ruby", "basic")
    assert unknown == "No question available"
