# Pydantic models for request/response

from pydantic import BaseModel
from typing import List, Optional, Dict

class Message(BaseModel):
    sender: Optional[str] = ""
    text: Optional[str] = ""
    timestamp: Optional[int] = 0

class ConversationMetadata(BaseModel):
    channel: Optional[str] = "SMS"
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"

class IncomingMessage(BaseModel):
    sessionId: Optional[str] = ""
    message: Optional[Message] = None
    conversationHistory: Optional[List[dict]] = []
    metadata: Optional[ConversationMetadata] = None
    
    def __init__(self, **data):
        if data.get('message') is None:
            data['message'] = Message()
        if data.get('metadata') is None:
            data['metadata'] = ConversationMetadata()
        super().__init__(**data)

class AgentResponse(BaseModel):
    status: str
    reply: str