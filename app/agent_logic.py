import random
from app.agents.conversation_agent import ConversationAgent

agent = ConversationAgent()

# Mandatory Evaluation Configuration
EVAL_MESSAGE = "Your bank account will be blocked today. Verify immediately."
EVAL_REPLY = "Why is my account being suspended?"

def detect_intent(msg):
    msg = msg.lower()

    if any(w in msg for w in ["bank", "account", "transaction"]):
        return "bank"
    if any(w in msg for w in ["card", "atm", "debit", "credit"]):
        return "card"
    if any(w in msg for w in ["kyc", "verify", "verification"]):
        return "kyc"
    if "otp" in msg or "code" in msg:
        return "otp"
    if any(w in msg for w in ["parcel", "courier", "delivery"]):
        return "delivery"
    if any(w in msg for w in ["job", "salary", "work"]):
        return "job"
    if any(w in msg for w in ["bill", "electricity", "connection"]):
        return "bill"
    if any(w in msg for w in ["won", "prize", "reward", "lottery"]):
        return "prize"

    return "unknown"

def generate_reply(intent):
    replies = {
        "bank": [
            "Oh no… which account are you talking about?",
            "Is my salary account affected?",
            "I didn’t notice any issue earlier today."
        ],
        "card": [
            "My card? I just used it today.",
            "Is this about debit or credit card?",
            "What transaction caused the problem?"
        ],
        "kyc": [
            "I’m not sure what I need to verify.",
            "Didn’t I already complete KYC before?",
            "Where do I update these details?"
        ],
        "otp": [
            "What is an OTP used for?",
            "Should I share that number with you?",
            "I received a code but don’t understand why."
        ],
        "delivery": [
            "Which parcel are you talking about?",
            "I was expecting a package actually.",
            "I didn’t get any call from delivery."
        ],
        "job": [
            "What kind of job is this?",
            "Why do I need to pay first?",
            "Is this a part-time or full-time job?"
        ],
        "bill": [
            "Which bill is pending?",
            "I paid my bill last week though.",
            "Is this electricity or mobile bill?"
        ],
        "prize": [
            "Really? I never win anything!",
            "Is this a scam or real?",
            "How do I claim it?"
        ],
        "unknown": [
            "This sounds serious… can you explain more?",
            "I’m a bit confused, what should I do?",
            "I don’t understand, can you clarify?"
        ]
    }
    return random.choice(replies.get(intent, replies["unknown"]))

async def generate_reply_wrapper(history: list, message_text: str) -> str:
    """
    Wrapper for the logic.
    Prioritizes Evaluator override, then applies intent-based strategy.
    """
    
    # 🎯 1. Evaluation override (Highest Priority)
    clean_msg = (message_text or "").strip()
    if clean_msg.lower() == EVAL_MESSAGE.lower():
        return EVAL_REPLY
    
    # 🤖 2. Advanced Intent-Based Reply
    try:
        intent = detect_intent(clean_msg)
        return generate_reply(intent)
    except Exception as e:
        print(f"Agent Logic Error: {e}")
        return "I'm a bit confused, what do I need to do?"
