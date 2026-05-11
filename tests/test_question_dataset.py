# tests/test_question_dataset.py - Unit tests for question templates.

from screening_ai.question_templates import (
    generate_skill_question,
    generate_experience_question,
    generate_location_question
)

def test_template():
    q_skill = generate_skill_question("Backend Developer")
    assert "Backend Developer" in q_skill
    assert q_skill == "What are your key skills relevant to the Backend Developer role?"

    q_exp = generate_experience_question("CNC Machinist")
    assert "CNC Machinist" in q_exp
    assert q_exp == "Can you describe your experience related to the CNC Machinist position?"

    q_loc = generate_location_question()
    assert q_loc == "Are you open to relocation or remote work?"
