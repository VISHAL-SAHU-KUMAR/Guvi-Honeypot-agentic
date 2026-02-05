from app.services.gemini_service import GeminiService
from app.config import settings
from typing import Tuple, List, Dict
import json
import logging

logger = logging.getLogger(__name__)

class ScamDetector:
    def __init__(self):
        self.gemini = GeminiService()
        self.scam_patterns = self._load_patterns()
    
    def _load_patterns(self) -> Dict:
        """Load scam patterns and dataset from data files"""
        try:
            with open('data/scam_patterns/full_dataset.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return {"scam_examples": [], "ham_examples": []}
    
    async def analyze(
        self, 
        message: str, 
        history: List[Dict],
        metadata: Dict
    ) -> Tuple[bool, float]:
        """Analyze message for scam intent with expanded dataset context"""
        
        # Quick pattern check for efficiency
        message_lower = message.lower()
        scam_keywords = ["otp", "urgent", "verify", "kyc", "blocked", "refund", "upi", "prize", "limit", "suspend"]
        
        matches = [kw for kw in scam_keywords if kw in message_lower]
        if matches:
            # High initial confidence if keywords match
            confidence = min(0.5 + (len(matches) * 0.1), 0.95)
        else:
            confidence = 0.2

        # In Mock/Fallback mode, use rule-based matching
        # In Gemini mode, use few-shot from the dataset
        prompt = self._create_detection_prompt(message, history, metadata)
        
        response = await self.gemini.generate_content(prompt, temperature=0.1)
        
        try:
            # Find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != -1:
                data = json.loads(response[start:end])
                return data.get('is_scam', False), data.get('confidence', 0.5)
        except:
            pass
            
        return confidence > 0.6, confidence
    
    def _create_detection_prompt(
        self, 
        message: str, 
        history: List[Dict],
        metadata: Dict
    ) -> str:
        """Create scam detection prompt for Claude"""
        
        patterns_str = json.dumps(self.scam_patterns, indent=2)
        history_str = "\n".join([
            f"{h['sender']}: {h['text']}" for h in history
        ])
        
        return f"""You are an expert scam detection system for India.

SCAM PATTERNS DATABASE:
{patterns_str}

CONVERSATION HISTORY:
{history_str}

CURRENT MESSAGE:
Sender: scammer
Text: {message}
Channel: {metadata.get('channel', 'Unknown')}
Language: {metadata.get('language', 'English')}

TASK:
Analyze if this message is a scam attempt. Consider:
1. Urgency tactics ("account blocked", "verify now")
2. Payment requests (UPI, bank account, OTP)
3. Impersonation (banks, government, delivery)
4. Phishing links
5. Indian context (Paytm, PhonePe, SBI, etc.)

OUTPUT FORMAT (JSON only):
{{
  "is_scam": true/false,
  "confidence": 0.0-1.0,
  "scam_type": "bank_fraud/upi_scam/phishing/fake_offer/other",
  "indicators": ["urgency", "payment_request", etc.],
  "reasoning": "brief explanation"
}}

Respond with ONLY the JSON, no additional text."""

    def _parse_detection_result(self, response_text: str) -> Dict:
        """Parse Claude's JSON response"""
        try:
            # Extract JSON from response
            result = json.loads(response_text.strip())
            return result
        except json.JSONDecodeError:
            # Fallback: use rule-based detection
            return self._fallback_detection(response_text)
    
    def _fallback_detection(self, message: str) -> Dict:
        """Rule-based fallback if JSON parsing fails"""
        message_lower = message.lower()
        
        urgency_count = sum(
            1 for keyword in self.scam_patterns['urgency_keywords']
            if keyword.lower() in message_lower
        )
        
        payment_count = sum(
            1 for keyword in self.scam_patterns['payment_keywords']
            if keyword.lower() in message_lower
        )
        
        is_scam = (urgency_count >= 2) or (payment_count >= 1 and urgency_count >= 1)
        confidence = min((urgency_count + payment_count) / 5.0, 1.0)
        
        return {
            "is_scam": is_scam,
            "confidence": confidence,
            "scam_type": "unknown",
            "indicators": ["rule_based_detection"]
        }