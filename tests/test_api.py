# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from unittest.mock import AsyncMock, patch

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "agentic-honeypot"}

@patch("app.agents.scam_detector.ScamDetector.analyze", new_callable=AsyncMock)
@patch("app.agents.conversation_agent.ConversationAgent.generate_response", new_callable=AsyncMock)
@patch("app.agents.conversation_agent.ConversationAgent.should_end_conversation", new_callable=AsyncMock)
def test_scam_detection_flow(mock_end, mock_generate, mock_analyze):
    # Setup mocks
    mock_analyze.return_value = (True, 0.95)
    mock_generate.return_value = "Oh no, my account is blocked? What should I do?"
    from app.models.intelligence import Intelligence
    mock_end.return_value = (False, Intelligence())
    
    payload = {
        "sessionId": "test-session-123",
        "message": {
            "sender": "scammer",
            "text": "Your SBI account is blocked. Verify at http://scam-link.com",
            "timestamp": 1700000000
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    headers = {"x-api-key": settings.API_KEY}
    
    response = client.post("/api/scam-detection", json=payload, headers=headers)
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "reply" in response.json()
    assert response.json()["reply"] == "Oh no, my account is blocked? What should I do?"

def test_invalid_api_key():
    payload = {
        "sessionId": "test",
        "message": {"sender": "u", "text": "h", "timestamp": 1},
        "conversationHistory": []
    }
    response = client.post("/api/scam-detection", json=payload, headers={"x-api-key": "wrong-key"})
    assert response.status_code == 401
