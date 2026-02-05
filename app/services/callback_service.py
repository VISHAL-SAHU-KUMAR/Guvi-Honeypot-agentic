
import httpx
from typing import Dict, Any
from app.config import settings
from app.models.intelligence import Intelligence
import logging

logger = logging.getLogger(__name__)

class CallbackService:
    CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    
    async def send_final_result(
        self,
        session_id: str,
        session_data: Dict,
        intelligence: Intelligence
    ):
        """Send final result to GUVI evaluation endpoint"""
        
        payload = {
            "sessionId": session_id,
            "scamDetected": session_data.get('is_scam', True),
            "totalMessagesExchanged": len(session_data.get('messages', [])),
            "extractedIntelligence": {
                "bankAccounts": intelligence.bankAccounts,
                "upiIds": intelligence.upiIds,
                "phishingLinks": intelligence.phishingLinks,
                "phoneNumbers": intelligence.phoneNumbers,
                "suspiciousKeywords": intelligence.suspiciousKeywords
            },
            "agentNotes": self._generate_agent_notes(session_data, intelligence)
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.CALLBACK_URL,
                    json=payload,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Successfully sent callback for session {session_id}")
                else:
                    logger.error(f"Callback failed: {response.status_code} - {response.text}")
                    
        except Exception as e:
            logger.error(f"Error sending callback: {e}")
    
    def _generate_agent_notes(self, session_data: Dict, intelligence: Intelligence) -> str:
        """Generate summary notes about scammer behavior"""
        
        notes = []
        
        if intelligence.bankAccounts:
            notes.append(f"Extracted {len(intelligence.bankAccounts)} bank account(s)")
        if intelligence.upiIds:
            notes.append(f"Extracted {len(intelligence.upiIds)} UPI ID(s)")
        if intelligence.phishingLinks:
            notes.append("Phishing links detected")
        
        tactics = intelligence.suspiciousKeywords[:3]
        if tactics:
            notes.append(f"Used tactics: {', '.join(tactics)}")
        
        return "; ".join(notes) if notes else "Scam engagement completed"