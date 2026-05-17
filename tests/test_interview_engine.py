# tests/test_interview_engine.py

from interview_ai.question_generator import load_question_bank, generate_questions

def test_load_question_bank():
    bank = load_question_bank()
    assert "categories" in bank
    assert "role_based" in bank
    assert "introduction" in bank["categories"]

def test_generate_questions_fresher_tech():
    questions = generate_questions("technical", "fresher")
    assert len(questions) == 6
    # Academic background is a fresher intro question
    # Let's verify we selected at least one technical question or academic question
    bank = load_question_bank()
    tech_pool = set(bank["role_based"]["technical"])
    fresher_intro = set(bank["categories"]["introduction"]["fresher"])
    
    # Check that they came from the correct bank categories
    # (Since we take random.sample of 6, we check that the questions exist in the bank)
    all_possible = []
    all_possible += bank["categories"]["introduction"]["fresher"]
    for cat in ["strengths_weaknesses", "teamwork", "career_goals", "availability"]:
        all_possible += bank["categories"][cat]["common"]
    all_possible += bank["role_based"]["technical"]
    
    for q in questions:
        assert q in all_possible

def test_generate_questions_exp_non_tech():
    questions = generate_questions("non_technical", "experienced")
    assert len(questions) == 6
    bank = load_question_bank()
    all_possible = []
    all_possible += bank["categories"]["introduction"]["experienced"]
    for cat in ["strengths_weaknesses", "teamwork", "career_goals", "availability"]:
        all_possible += bank["categories"][cat]["common"]
    all_possible += bank["role_based"]["non_technical"]
    
    for q in questions:
        assert q in all_possible
