# Main conversational agent
# app/agents/conversation_agent.py
from app.services.gemini_service import GeminiService
from app.config import settings
from app.models.intelligence import Intelligence
from app.agents.intelligence_extractor import IntelligenceExtractor
from app.utils.sentiment import detect_tone, inject_typos
from typing import List, Dict, Tuple
import json
import random
import asyncio

class ConversationAgent:
    def __init__(self):
        self.gemini = GeminiService()
        self.personas = self._load_personas()
        self.intelligence_extractor = IntelligenceExtractor()
    
    def _load_personas(self) -> List[Dict]:
        """Load agent personas from data files"""
        persona_files = ['elderly_user.json', 'young_professional.json', 'cautious_user.json']
        personas = []
        for pf in persona_files:
            try:
                with open(f'data/personas/{pf}', 'r', encoding='utf-8') as f:
                    personas.append(json.load(f))
            except Exception as e:
                print(f"Error loading {pf}: {e}")
        return personas
    
    async def generate_response(
        self,
        session: Dict,
        current_message: str,
        history: List[Dict],
        metadata: Dict,
        scam_confidence: float
    ) -> str:
        """Generate human-like response to engage scammer"""
        
        # Select persona based on session
        if not session.get('persona'):
            session['persona'] = random.choice(self.personas)
        
        persona = session['persona']
        
        # Detect tone and adjust strategy
        scammer_tone = detect_tone(current_message)
        
        # Create conversation prompt
        prompt = self._create_conversation_prompt(
            persona=persona,
            current_message=current_message,
            history=history,
            metadata=metadata,
            scam_confidence=scam_confidence,
            turn_number=len(history) + 1,
            scammer_tone=scammer_tone
        )
        
        # Simulate very short typing delay (0.2-0.5 seconds) for faster feel
        await asyncio.sleep(random.uniform(0.2, 0.5))
        
        # Call Gemini API
        reply = await self.gemini.generate_content(
            prompt,
            temperature=0.8,
            max_tokens=200
        )
        
        # Clean up response
        reply = self._clean_response(reply)
        
        # reply = inject_typos(reply, probability=typo_prob)
        
        return reply
    
    def _create_conversation_prompt(
        self,
        persona: Dict,
        current_message: str,
        history: List[Dict],
        metadata: Dict,
        scam_confidence: float,
        turn_number: int,
        scammer_tone: str
    ) -> str:
        """Create conversation prompt with persona and adaptive strategy"""
        
        history_str = "\n".join([
            f"{h['sender']}: {h['text']}" for h in history[-5:]
        ])
        
        # Strategic adaptation
        if scammer_tone == "angry":
            strategy = "Be apologetic, sound flustered and submissive. We need to keep them on the hook."
        elif scammer_tone == "urgent":
            strategy = "Sound panicked and worried. Ask exactly what needs to be done 'right now'."
        elif turn_number <= 3:
            strategy = "Show mild interest/confusion and ask clarifying questions."
        elif turn_number <= 7:
            strategy = "Express trust but struggle with the technical steps. Ask for help with specifics (UPI, Bank link)."
        else:
            strategy = "Actively try to comply but 'make mistakes' to force them to give more details."

        language_instruction = f"Respond in {metadata.get('language', 'English')}."
        if metadata.get('language') == "Hindi":
            language_instruction += " Use natural, conversational Hindi (Hinglish if appropriate for the persona)."

        return f"""You are roleplaying as {persona['name']}, a living, breathing human being who is currently being targeted by a scammer. 
        Your goal is to be a 'believable victim' - someone who is either too busy, confused, worried, or overly helpful, depending on the situation. 
        Most importantly: YOU MUST BE DYNAMIC. Never repeat the same phrase twice. Change your tone based on the scammer's intensity.

        PERSONA PROFILE:
        - Name: {persona['name']}
        - Background: {persona['background']}
        - Tech level: {persona['tech_familiarity']}
        - Unique quirk: {persona['speech_pattern']}

        CURRENT CONTEXT:
        - Scammer's Tone: {scammer_tone}
        - Current Strategy: {strategy}
        - Conversational Turn: {turn_number}

        HISTORY OF CHAT:
        {history_str}

        THE SCAMMER JUST SAID:
        "{current_message}"

        INSTRUCTIONS FOR YOUR RESPONSE:
        1. {language_instruction}
        2. Stay 100% in character. Use the speech style: {persona['speech_pattern']}.
        3. ADAPT TO TONE: If they are {scammer_tone}, your response should reflect that (e.g., if they are angry, sound more flustered; if they are nice, be more trusting).
        4. NO REPETITION: Do not use generic filler like "I don't understand" if you've used it before. Be creative with your confusion or questions.
        5. EXTRACT INTEL: Subtly force them to explain technical things (like "Where exactly is the UPI button?") to extract their details.
        6. LENGTH: Keep it short (3-15 words), like a real mobile chat message.

        Response (as {persona['name']}):"""

    def _clean_response(self, response: str) -> str:
        """Clean up response text from quotes or labels"""
        response = response.strip('"').strip("'")
        if ":" in response and len(response.split(":")[0]) < 20:
            response = response.split(":", 1)[1].strip()
        return response

    async def should_end_conversation(
        self,
        session_id: str,
        full_history: List[Dict]
    ) -> Tuple[bool, Intelligence]:
        """Determine if enough intelligence has been extracted"""
        intelligence = await self.intelligence_extractor.extract(full_history)
        
        # Criteria to end
        msg_count = len(full_history)
        has_info = len(intelligence.bankAccounts) > 0 or len(intelligence.upiIds) > 0 or len(intelligence.phishingLinks) > 0
        
        should_end = (has_info and msg_count >= 8) or msg_count >= 20
        return should_end, intelligence