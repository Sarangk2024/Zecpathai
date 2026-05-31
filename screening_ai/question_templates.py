# screening_ai/question_templates.py - Dynamic template generators and dataset loaders.

import json
import os

def generate_skill_question(role):
    return f"What are your key skills relevant to the {role} role?"

def generate_experience_question(role):
    return f"Can you describe your experience related to the {role} position?"

def generate_location_question():
    return "Are you open to relocation or remote work?"

def load_questions(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
