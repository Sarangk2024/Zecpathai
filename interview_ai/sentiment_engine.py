# interview_ai/sentiment_engine.py

POSITIVE = ["confident", "strong", "good", "success", "achieved"]
NEGATIVE = ["difficult", "problem", "struggle", "fail", "weak"]

def sentiment_score(text):
    text = text.lower()
    pos = sum(word in text for word in POSITIVE)
    neg = sum(word in text for word in NEGATIVE)
    
    if pos > neg:
        sentiment = "Positive"
        score = min(pos / 5, 1.0)
    elif neg > pos:
        sentiment = "Negative"
        score = min(neg / 5, 1.0)
    else:
        sentiment = "Neutral"
        score = 0.5
        
    return {
        "sentiment": sentiment,
        "sentiment_score": round(score, 2)
    }
