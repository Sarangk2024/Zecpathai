# technical_ai/question_generator.py

import random

QUESTION_BANK = {
    "JavaScript": {
        "basic": ["What is a variable?", "Explain let vs var"],
        "intermediate": ["Explain closures", "How does event loop work?"],
        "advanced": ["Design scalable frontend architecture"]
    },
    "Python": {
        "basic": ["What is a list?", "Explain loops"],
        "intermediate": ["Explain decorators", "How does GIL work?"],
        "advanced": ["Design scalable backend system"]
    }
}

def generate_question(skill, difficulty):
    questions = QUESTION_BANK.get(skill, {}).get(difficulty, ["No question available"])
    return random.choice(questions)
