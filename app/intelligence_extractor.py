import re

def extract_intelligence(text):
    phone_pattern = r"\b\d{10}\b"
    upi_pattern = r"\b[\w.-]+@[\w]+\b"
    url_pattern = r"http[s]?://\S+"
    # Standard Indian Bank Account pattern: 9 to 18 digits
    bank_pattern = r"\b\d{11,18}\b"

    phones = re.findall(phone_pattern, text)
    upis = re.findall(upi_pattern, text)
    urls = re.findall(url_pattern, text)
    banks = re.findall(bank_pattern, text)

    text_lower = text.lower()
    keywords = [w for w in ["otp","verify","urgent","blocked","refund","account"] if w in text_lower]

    return {
        "bankAccounts": banks,
        "upiIds": upis,
        "phishingLinks": urls,
        "phoneNumbers": phones,
        "suspiciousKeywords": keywords
    }
