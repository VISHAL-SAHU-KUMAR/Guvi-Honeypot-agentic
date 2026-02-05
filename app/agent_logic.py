from app.agents.conversation_agent import ConversationAgent
import asyncio

agent = ConversationAgent()

def generate_reply(history: list, message_text: str) -> str:
    """Wrapper for the AI-based agent response generation logic for Hackathon scoring."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Create a mock session object
        session = {'messages': history}
        metadata = {'channel': 'SMS', 'language': 'English'}
        
        reply = loop.run_until_complete(agent.generate_response(
            session=session,
            current_message=message_text,
            history=history,
            metadata=metadata,
            scam_confidence=0.9
        ))
        return reply
    except:
        return "I'm a bit confused, what do I need to do?"
