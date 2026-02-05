
from typing import Dict, Optional
import json
from datetime import datetime

class SessionManager:
    def __init__(self):
        self.sessions = {}  # In production, use Redis
    
    async def get_or_create_session(
        self, 
        session_id: str, 
        is_scam: bool = False
    ) -> Dict:
        """Get existing session or create new one"""
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'session_id': session_id,
                'created_at': datetime.now().isoformat(),
                'is_scam': is_scam,
                'messages': [],
                'persona': None,
                'intelligence': {
                    'bankAccounts': [],
                    'upiIds': [],
                    'phoneNumbers': [],
                    'phishingLinks': [],
                    'suspiciousKeywords': []
                }
            }
        
        return self.sessions[session_id]
    
    async def update_session(
        self,
        session_id: str,
        message: str,
        reply: str,
        sender: str
    ):
        """Update session with new message"""
        if session_id in self.sessions:
            self.sessions[session_id]['messages'].append({
                'sender': sender,
                'message': message,
                'reply': reply,
                'timestamp': datetime.now().isoformat()
            })
    
    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data"""
        return self.sessions.get(session_id)