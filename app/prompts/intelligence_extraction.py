# app/prompts/intelligence_extraction.py

INTELLIGENCE_EXTRACTION_PROMPT = """Extract ALL scam-related intelligence from this conversation.

CONVERSATION:
{full_text}

EXTRACT:
1. Bank account numbers (Indian format: XXXX-XXXX-XXXX or similar)
2. UPI IDs (format: user@bankname or phonenumber@upi)
3. Phone numbers (Indian: +91XXXXXXXXXX or 10 digits)
4. Phishing/suspicious links (any URLs)
5. Suspicious keywords used

OUTPUT FORMAT (JSON only):
{{
  "bankAccounts": ["account1", "account2"],
  "upiIds": ["upi1@bank", "upi2@paytm"],
  "phoneNumbers": ["+91XXXXXXXXXX"],
  "phishingLinks": ["http://example.com"],
  "suspiciousKeywords": ["urgent", "blocked", "verify"]
}}

Be thorough. Extract even partial information. Respond with ONLY JSON."""
