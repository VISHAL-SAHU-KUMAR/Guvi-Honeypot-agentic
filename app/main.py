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


@app.post("/api/scam-detection", response_model=AgentResponse)
@app.post("/honeypot", response_model=AgentResponse)
@limiter.limit("100/minute")
async def detect_and_engage(
    request: Request,
    payload: IncomingMessage,
    x_api_key: str = Header(...)
):
    """Main API endpoint for scam detection and engagement"""
    
    # Validate API key
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        session_id = payload.sessionId
        message = payload.message
        history = payload.conversationHistory
        
        # Step 1: Detect scam intent
        is_scam, confidence = await scam_detector.analyze(
            message.text, 
            history,
            payload.metadata.dict() if payload.metadata else {}
        )
        
        # Step 2: Get or create session
        session = await session_manager.get_or_create_session(
            session_id, 
            is_scam=is_scam
        )
        
        # Step 3: Generate agent response
        agent_reply = await conversation_agent.generate_response(
            session=session,
            current_message=message.text,
            history=history,
            metadata=payload.metadata.dict() if payload.metadata else {},
            scam_confidence=confidence
        )
        
        # Step 4: Update session
        await session_manager.update_session(
            session_id,
            message=message.text,
            reply=agent_reply,
            sender="user"
        )
        
        # Step 5: Check if conversation should end
        # We use a copy of history + new user message
        full_history = history + [{"sender": "scammer", "text": message.text}, {"sender": "user", "text": agent_reply}]
        should_end, intelligence = await conversation_agent.should_end_conversation(
            session_id, full_history
        )
        
        # Step 6: Store latest intelligence in session
        session['intelligence'] = intelligence
        
        if should_end and is_scam:
            # Send final callback to GUVI
            await callback_service.send_final_result(
                session_id=session_id,
                session_data=session,
                intelligence=intelligence
            )
        
        return AgentResponse(
            status="success",
            reply=agent_reply
        )
        
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        error_msg = str(e)
        if "quota" in error_msg.lower() or "limit" in error_msg.lower():
            detail = "Gemini API Quota exceeded. Please check your Google Cloud Console."
        elif "API key" in error_msg:
            detail = "Gemini API Key is invalid or expired."
        else:
            detail = error_msg
        raise HTTPException(status_code=500, detail=detail)


@app.get("/api/session-intelligence/{session_id}")
async def get_session_intelligence(session_id: str, x_api_key: str = Header(None)):
    """Live intelligence polling for UI"""
    try:
        if x_api_key != settings.API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        session = await session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        intel = session.get('intelligence', {})
        
        # Super defensive conversion
        intel_dict = {}
        if hasattr(intel, 'model_dump'):
            try: intel_dict = intel.model_dump()
            except: pass
        if not intel_dict and hasattr(intel, 'dict'):
            try: intel_dict = intel.dict()
            except: pass
        if not intel_dict and isinstance(intel, dict):
            intel_dict = intel
            
        return {
            "status": "success",
            "intelligence": intel_dict,
            "isScam": session.get('is_scam', False),
            "messageCount": len(session.get('messages', []))
        }
    except Exception as e:
        logger.error(f"Intelligence Endpoint Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
@app.get("/healthz")
async def health_check():
    return {"status": "ok"}