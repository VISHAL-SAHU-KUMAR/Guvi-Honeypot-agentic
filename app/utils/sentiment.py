# app/utils/sentiment.py
from textblob import TextBlob
import random

def analyze_sentiment(text: str) -> float:
    """Returns polarity from -1.0 (negative) to 1.0 (positive)"""
    try:
        blob = TextBlob(text)
        return blob.sentiment.polarity
    except:
        return 0.0

def detect_tone(text: str) -> str:
    """Detects simple tone of the message"""
    sentiment = analyze_sentiment(text)
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['urgent', 'immediately', 'now', 'quickly']):
        return "urgent"
    if any(word in text_lower for word in ['stupid', 'idiot', 'waste', 'listen']):
        return "angry"
    if sentiment < -0.3:
        return "negative/hostile"
    if sentiment > 0.3:
        return "positive/friendly"
    return "neutral"

def inject_typos(text: str, probability: float = 0.05) -> str:
    """Randomly swaps or omit characters to simulate human typing"""
    if probability <= 0:
        return text
        
    chars = list(text)
    for i in range(len(chars) - 1):
        if random.random() < probability:
            # Swap with next char
            chars[i], chars[i+1] = chars[i+1], chars[i]
            
    return "".join(chars)
