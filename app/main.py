# app/main.py
from fastapi import FastAPI, Header, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import IncomingMessage, AgentResponse
from app.agents.scam_detector import ScamDetector
from app.agents.conversation_agent import ConversationAgent
from app.services.session_manager import SessionManager
from app.services.callback_service import CallbackService
from app.config import settings
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.utils.logger import setup_logger
import logging
import os
import requests
from .intelligence_extractor import extract_intelligence
from .scam_detector import is_scam
from .agent_logic import generate_reply

# Mandatory Scoring Config
GUVI_CALLBACK_URL = os.getenv("GUVI_CALLBACK_URL", "https://hackathon.guvi.in/api/updateHoneyPotFinalResult")
session_memory = {}

# Initialize app and Limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Agentic Honey-Pot API", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Static UI serving
@app.get("/", include_in_schema=False)
async def get_ui():
    return FileResponse("index.html")

# Setup Logger
logger = setup_logger("main")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
scam_detector = ScamDetector()
conversation_agent = ConversationAgent()
session_manager = SessionManager()
callback_service = CallbackService()


@app.post("/api/scam-detection")
@app.post("/honeypot")
@limiter.limit("100/minute")
async def detect_and_engage(
    request: Request,
    payload: IncomingMessage,
    x_api_key: str = Header(...)
):
    """Refactored endpoint to match Hackathon Scoring Requirement #2 & #8"""
    
    # 1. Validate API key
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    session_id = payload.sessionId
    message_text = payload.message.text
    history = payload.conversationHistory
    
    # 2. Process message through mandatory logic
    scam = await is_scam(message_text)
    intel = extract_intelligence(message_text)
    
    # 3. Maintain session memory for scoring
    if session_id not in session_memory:
        session_memory[session_id] = {
            "messages": 0,
            "intel": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": []
            }
        }
    
    session_memory[session_id]["messages"] += 1
    
    # Update intelligence buffer (Mandatory Requirement #7)
    for key in intel:
        if isinstance(intel[key], list):
            for item in intel[key]:
                if item not in session_memory[session_id]["intel"][key]:
                    session_memory[session_id]["intel"][key].append(item)
    
    # 4. Generate AI reply (Mandatory Requirement #5)
    reply = await generate_reply(history, message_text)
    
    # 5. 🎯 Mandatory Trigger: After 3 messages, send callback (Requirement #8)
    if scam and session_memory[session_id]["messages"] >= 3:
        send_final_callback(session_id)
        
    return {
        "status": "success",
        "reply": reply,
        "isScam": scam,
        "messageCount": session_memory[session_id]["messages"]
    }

def send_final_callback(session_id):
    """Mandatory Callback Function for Hackathon Scoring Requirement #8"""
    data = session_memory.get(session_id)
    if not data:
        return

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": data["messages"],
        "extractedIntelligence": data["intel"],
        "agentNotes": "Scammer engagement threshold reached. Strategic extraction complete."
    }

    try:
        response = requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            logger.info(f"GUVI callback sent successfully for session {session_id}")
        else:
            logger.error(f"Callback failed: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Callback failed: {e}")

@app.get("/api/session-intelligence/{session_id}")
async def get_intel(session_id: str, x_api_key: str = Header(...)):
    """Live intelligence polling for UI powered by session_memory"""
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    data = session_memory.get(session_id)
    if not data:
        return {"status": "error", "message": "Session not found"}
        
    return {
        "status": "success",
        "intelligence": data["intel"],
        "isScam": True if data["intel"]["suspiciousKeywords"] else False,
        "messageCount": data["messages"]
    }

@app.get("/health")
@app.get("/healthz")
async def health_check():
    return {"status": "ok"}