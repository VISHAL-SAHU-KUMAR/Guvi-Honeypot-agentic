from app.services.gemini_service import GeminiService
from app.config import settings
from app.models.intelligence import Intelligence
from typing import List, Dict
import re
import json

class IntelligenceExtractor:
    def __init__(self):
        self.gemini = GeminiService()
    
    async def extract(self, conversation_history: List[Dict]) -> Intelligence:
        """Extract all intelligence from conversation"""
        
        # Combine all messages
        full_text = "\n".join([
            f"{msg['sender']}: {msg['text']}" 
            for msg in conversation_history
        ])
        
        # Use Gemini for intelligent extraction
        prompt = f"""Extract ALL scam-related intelligence from this conversation.

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

        response_text = await self.gemini.generate_content(
            prompt,
            temperature=0.0,
            max_tokens=800
        )
        
        # Parse response
        try:
            # Clean up potential markdown formatting in response
            clean_text = response_text.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_text)
        except:
            # Fallback to regex extraction
            data = self._regex_fallback_extraction(full_text)
        
        # Also do regex-based extraction and merge
        regex_data = self._regex_fallback_extraction(full_text)
        
        # Merge results
        intelligence = Intelligence(
            bankAccounts=list(set(data.get('bankAccounts', []) + regex_data.get('bankAccounts', []))),
            upiIds=list(set(data.get('upiIds', []) + regex_data.get('upiIds', []))),
            phoneNumbers=list(set(data.get('phoneNumbers', []) + regex_data.get('phoneNumbers', []))),
            phishingLinks=list(set(data.get('phishingLinks', []) + regex_data.get('phishingLinks', []))),
            suspiciousKeywords=list(set(data.get('suspiciousKeywords', []) + regex_data.get('suspiciousKeywords', [])))
        )
        
        return intelligence
    
    def _regex_fallback_extraction(self, text: str) -> Dict:
        """Regex-based extraction as fallback"""
        
        # Bank accounts: various Indian formats
        bank_accounts = re.findall(r'\b\d{9,18}\b', text)
        
        # UPI IDs
        upi_ids = re.findall(r'\b[\w\.-]+@[\w\.-]+\b', text)
        upi_ids = [u for u in upi_ids if any(bank in u.lower() for bank in 
                   ['paytm', 'phonepe', 'googlepay', 'bhim', 'sbi', 'hdfc', 'icici', 'axis', 'ybl', 'okicici', 'oksbi'])]
        
        # Phone numbers
        phone_numbers = re.findall(r'(\+91[\s-]?)?[6-9]\d{9}\b', text)
        
        # URLs
        phishing_links = re.findall(r'https?://[^\s]+', text)
        
        # Suspicious keywords
        suspicious_keywords = []
        patterns = ['urgent', 'blocked', 'verify', 'suspend', 'immediate', 'expire', 'limited', 'account', 'payment']
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                suspicious_keywords.append(pattern)
        
        return {
            'bankAccounts': bank_accounts,
            'upiIds': upi_ids,
            'phoneNumbers': phone_numbers,
            'phishingLinks': phishing_links,
            'suspiciousKeywords': suspicious_keywords
        }