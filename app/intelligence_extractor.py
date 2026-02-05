import re

def extract_intelligence(text):
    """
    Mandatory Regex-based intelligence extraction for Hackathon scoring.
    Extracts phone numbers, UPI IDs, and phishing links.
    """
    phone_pattern = r"\b\d{10}\b"
    upi_pattern = r"\b[\w.-]+@[\w]+\b"
    url_pattern = r"http[s]?://\S+"

    text_lower = text.lower()

    return {
        "bankAccounts": [],
        "upiIds": re.findall(upi_pattern, text),
        "phishingLinks": re.findall(url_pattern, text),
        "phoneNumbers": re.findall(phone_pattern, text),
        "suspiciousKeywords": [w for w in ["otp","verify","urgent","blocked","refund"] if w in text_lower]
    }
