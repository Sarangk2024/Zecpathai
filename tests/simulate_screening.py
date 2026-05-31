# tests/simulate_screening.py

from screening_ai.scoring_engine import screening_scoring_pipeline

def simulate_test():
    sample_answers = [
        {
            "question_id": "Q3",
            "original_text": "I have 2 years experience",
            "intent": "experience",
            "skills": [],
            "experience_years": 2,
            "availability": "Unknown",
            "off_topic": False,
            "is_vague": False
        }
    ]
    intent_map = {"Q3": "experience"}
    result = screening_scoring_pipeline(sample_answers, intent_map)
    return result

if __name__ == "__main__":
    print(simulate_test())
