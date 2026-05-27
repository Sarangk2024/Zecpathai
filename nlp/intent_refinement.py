# nlp/intent_refinement.py

def refined_intent_detection(text):
    if not text:
        return "generic"
    text = text.lower()
    if any(word in text for word in ["built", "developed", "implemented", "experience"]):
        return "experience"
    if any(word in text for word in ["learned", "studied", "course", "degree"]):
        return "education"
    if any(word in text for word in ["will", "plan", "future"]):
        return "future_intent"
    return "generic"
