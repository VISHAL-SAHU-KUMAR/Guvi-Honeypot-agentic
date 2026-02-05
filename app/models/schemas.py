# Pydantic models for request/response

from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class ConversationMetadata(BaseModel):
    channel: Optional[str] = "SMS"
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"

class IncomingMessage(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[dict] = []
    metadata: Optional[ConversationMetadata] = None

class AgentResponse(BaseModel):
    status: str
    reply: str