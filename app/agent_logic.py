from app.agents.conversation_agent import ConversationAgent

agent = ConversationAgent()

async def generate_reply(history: list, message_text: str) -> str:
    """Wrapper for the AI-based agent response generation logic for Hackathon scoring."""
    try:
        # Create a mock session object
        session = {'messages': history}
        metadata = {'channel': 'SMS', 'language': 'English'}
        
        reply = await agent.generate_response(
            session=session,
            current_message=message_text,
            history=history,
            metadata=metadata,
            scam_confidence=0.9
        )
        return reply
    except Exception as e:
        print(f"Agent Logic Error: {e}")
        return "I'm a bit confused, what do I need to do?"
