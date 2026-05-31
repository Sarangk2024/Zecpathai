# screening_ai/intent_classifier.py - Standalone intent classifier utility.

from screening_ai.answer_engine import classify_intent

def get_intent(text):
    return classify_intent(text)
