import re

def extract_intelligence(text):
    phone_pattern = r"\b\d{10}\b"
    upi_pattern = r"\b[\w.-]+@[\w]+\b"
    url_pattern = r"http[s]?://\S+"

    phones = re.findall(phone_pattern, text)
    upis = re.findall(upi_pattern, text)
    urls = re.findall(url_pattern, text)

    text_lower = text.lower()
    keywords = [w for w in ["otp","verify","urgent","blocked","refund","account"] if w in text_lower]

    return {
        "bankAccounts": [],        # Only for real bank patterns if you add later
        "upiIds": upis,
        "phishingLinks": urls,
        "phoneNumbers": phones,
        "suspiciousKeywords": keywords
    }
