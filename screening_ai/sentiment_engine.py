# screening_ai/sentiment_engine.py

# -------------------------------
# Simple Sentiment Word Lists
# -------------------------------
POSITIVE_WORDS = ["good", "great", "confident", "skilled", "experienced", "strong"]
NEGATIVE_WORDS = ["weak", "bad", "difficult", "problem", "not sure", "struggle"]

# -------------------------------
# Sentiment Detection
# -------------------------------
def detect_sentiment(text):
    text = text.lower()
    pos_count = sum(word in text for word in POSITIVE_WORDS)
    neg_count = sum(word in text for word in NEGATIVE_WORDS)
    if pos_count > neg_count:
        sentiment = "Positive"
        score = min(pos_count / 5, 1.0)
    elif neg_count > pos_count:
        sentiment = "Negative"
        score = min(neg_count / 5, 1.0)
    else:
        sentiment = "Neutral"
        score = 0.5
    return {
        "sentiment": sentiment,
        "sentiment_score": round(score, 2)
    }
