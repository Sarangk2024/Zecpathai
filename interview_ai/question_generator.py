# interview_ai/question_generator.py

import os
import json
import random

def load_question_bank():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    bank_path = os.path.join(dir_path, "question_bank.json")
    with open(bank_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_questions(role_type, experience_level):
    qb = load_question_bank()
    questions = []
    
    # Introduction
    questions += qb["categories"]["introduction"].get(experience_level, [])
    
    # Common categories
    for cat in ["strengths_weaknesses", "teamwork", "career_goals", "availability"]:
        questions += qb["categories"][cat]["common"]
        
    # Role-based
    questions += qb["role_based"].get(role_type, [])
    
    # We want to be deterministic in tests if needed, but random.sample is requested
    # Let's use a stable seed or just standard sample
    return random.sample(questions, min(6, len(questions)))
