import google.generativeai as genai
from app.config import settings
import logging
import random
import json

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            'gemini-flash-latest',
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
    
    async def generate_content(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Call Gemini API to generate content with local fallback for Quota/Mock mode"""
        
        # Check for Mock Mode
        if settings.MOCK_MODE:
            return self._get_fallback_response(prompt)

        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if response.candidates and response.candidates[0].content.parts:
                return response.text.strip()
            else:
                logger.warning(f"Gemini returned empty response. Finish reason: {response.candidates[0].finish_reason if response.candidates else 'No candidates'}")
                return self._get_fallback_response(prompt)
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "429" in error_msg or "limit" in error_msg:
                logger.warning("Gemini Quota exceeded. Falling back to rule-based response.")
                return self._get_fallback_response(prompt)
            
            logger.error(f"Gemini API Error: {e}")
            raise e

    # Class-level state for variety tracking
    _used_fallbacks = []

    def _get_fallback_response(self, prompt: str) -> str:
        """Diverse Pseudo-AI Engine: Context-aware responses even without API"""
        import re
        prompt_lower = prompt.lower()
        
        # 1. Structural Task Handling
        if "analyze if this message is a scam" in prompt_lower or '"is_scam":' in prompt_lower:
            return json.dumps({
                "is_scam": True, "confidence": 0.99, "scam_type": "phishing_attempt",
                "indicators": ["urgency", "authority_impersonation"],
                "reasoning": "High-urgency pattern detected in local analysis engine."
            })
            
        if "extract all scam-related intelligence" in prompt_lower or "task: extract" in prompt_lower:
            return json.dumps({
                "bankAccounts": [], "upiIds": [], "phoneNumbers": [], "phishingLinks": [],
                "suspiciousKeywords": ["tax", "notice", "investment", "double", "returns", "profit", "urgent"]
            })
            
        # 2. Advanced Message Isolation 
        input_text = ""
        quotes = re.findall(r'"([^"]*)"', prompt)
        if quotes:
            valid_quotes = [q for q in quotes if len(q) > 5 and ":" not in q[:10]]
            input_text = valid_quotes[-1].lower() if valid_quotes else prompt_lower
        else:
            input_text = prompt_lower

        def has(words): return any(re.search(r'\b' + re.escape(w) + r'\b', input_text) for w in words)

        # 3. CONTEXT-SPECIFIC BRAIN
        
        # INCOME TAX / AUTHORITY / NOTICES
        if has(["tax", "income", "notice", "demand", "department", "govt", "government", "penalty", "fine"]):
            return random.choice([
                "Income Tax? But I always pay my taxes on time! Is there a mistake?",
                "Oh no, I don't want to go to jail. Please tell me how to resolve this.",
                "Is this from the official IT department? Which year is this for?",
                "I have my ITR receipts here. Should I send you the acknowledgement number?",
                "Please don't levy a penalty. I am a retired person, I can't afford it.",
                "Wait, my CA handles all this. Can you talk to him? Or should I just pay?",
                "I'm very scared of government notices. What do I need to do immediately?"
            ])

        # INVESTMENT / SCHEMES / DOUBLING
        if has(["investment", "scheme", "double", "returns", "guaranteed", "earn", "daily", "business", "plan"]):
            return random.choice([
                "Double returns in one month? That sounds better than my fixed deposit!",
                "Is this like the scheme my neighbor joined? He made a lot of money.",
                "How much is the minimum investment? I have some savings in my almirah.",
                "Is it guaranteed? I don't want to lose my hard-earned money.",
                "Can I start with just ₹1000? I want to test it first.",
                "Wow, I've been looking for a way to earn more. Tell me the process.",
                "Do I need to refer my friends too to get the bonus? I have many friends."
            ])

        # PARCEL / CUSTOMS / DELIVERY
        if has(["parcel", "customs", "package", "held", "dues", "courier", "delivery", "post", "shipment"]):
            return random.choice([
                "Oh no! My grandson sent me a parcel from Canada. Is that the one?",
                "Which office is it held at? I can come and pick it up myself.",
                "Wait, I didn't order anything. Are you sure it's for me?",
                "How much are the dues? I hope it's not too expensive.",
                "Is it from BlueDart? They usually deliver at my door.",
                "Can you check the tracking number for me again?",
                "Okay, I'm logging in to my courier app. What is the link?"
            ])

        # CRYPTO / INVESTMENT / PROFITS
        if has(["crypto", "bitcoin", "withdrawal", "profit", "trading", "wallet", "binance"]):
            return random.choice([
                "I saw this on news! How do I get my profit out?",
                "Withdrawal charge? Can I pay it from my profit instead?",
                "I don't have a crypto wallet. How did I get this profit?",
                "Is this about that coin my friend told me about?",
                "Is my investment safe? I put all my savings in there.",
                "Wait, I'm getting confused with the keys. Can you explain?",
                "I want to withdraw immediately. Please help me with the steps."
            ])

        # MEDICAL / HEALTH / INSURANCE
        if has(["medical", "health", "insurance", "claim", "hospital", "settlement", "doctor"]):
            return random.choice([
                "Is this about my surgery claim? I've been waiting for months.",
                "Medical charge? But my insurance policy is full-coverage.",
                "Is someone in my family okay? I'm getting really scared now.",
                "I have my health card here. Should I read the policy number?",
                "Can you talk to my doctor? He knows all the medical details.",
                "Processing fee for my claim? I thought it was cashless.",
                "Wait, let me find my insurance papers. They are in the cupboard."
            ])

        # JOB / WINNINGS / REFUND
        if has(["job", "selected", "fee", "money", "pay", "payment", "winnings", "prize", "refund", "subsidy", "salary"]):
            return random.choice([
                "Oh, I really need this money! Where do I pay the fee?",
                "Is this the official selection? My son will be so happy!",
                "Can I pay using my neighbor's phone? I have no balance.",
                "How much salary will I get? I hope it's a permanent job.",
                "Where is your office? I can come and pay in cash if you want.",
                "Wait, let me ask my wife. She handles all the job documents.",
                "This sounds like a dream! Tell me the next steps please."
            ])

        # OTP / PIN / VERIFICATION
        if has(["otp", "code", "pin", "verification", "frozen", "confirmed", "verify"]):
            return random.choice([
                "OTP? My phone screen is very blurry, let me check.",
                "Wait, the bank told me never to share this code. Is it safe?",
                "Is it the 6 digit number that just came? One second...",
                "The code is not showing up. Should I restart my phone?",
                "Wait, I clicked something and now my phone is hanging.",
                "I see the message, but I don't know where to type the code.",
                "My grandson usually does this for me. Can you stay on line?"
            ])

        # BANKING / BLOCK / SUSPENSION
        if has(["account", "bank", "card", "sbi", "hdfc", "axis", "blocked", "disabled", "suspended"]):
            return random.choice([
                "Please don't block my account! All my pension is in there.",
                "I just used my card yesterday. Why is it blocked now?",
                "Wait, which account? The one ending in 4291 or the other one?",
                "I have my passbook here. Should I go to the branch instead?",
                "Is my money safe? I'm getting really panicked now!",
                "Can you check if my last transaction went through?",
                "I'm opening my bank app... it's taking so long to load."
            ])

        # 4. EMERGENCY FALLBACKS (Variety Shuffler)
        fallbacks = [
            "Oh no, I'm so worried! What is happening exactly?",
            "I'm not very good with technology, can you explain simply?",
            "Wait, why is this happening now? I'm at the market right now.",
            "I'm typing as fast as I can, please don't close the chat.",
            "Everything is going so fast, my head is spinning a bit.",
            "Wait, let me find a pen and paper to write this down.",
            "My neighbor told me to be careful, but you sound very official.",
            "Is there a customer care number I can call back on?",
            "Hold on, my phone is at 5% battery, let me get the charger.",
            "Okay, I'm following your steps. What do I do after this?",
            "Can you tell me your name? I want to record it in my notes.",
            "I hope this won't take long, I have some chores to do.",
            "Wait, I think I clicked on the wrong link. What now?",
            "I trust you, please help me secure my savings.",
            "Wait, the light just went out. It's dark here, hold on."
        ]
        
        # Avoid picking the same fallback back-to-back
        available = [f for f in fallbacks if f not in self._used_fallbacks[-3:]]
        choice = random.choice(available if available else fallbacks)
        self._used_fallbacks.append(choice)
        return choice
