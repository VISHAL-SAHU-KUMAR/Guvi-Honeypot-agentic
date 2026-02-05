import asyncio
import random
from app.agent_logic import generate_reply, EVAL_MESSAGE, EVAL_REPLY, REPLY_BANKS

async def verify():
    print("--- Verifying Honeypot Logic ---")
    
    # Test Case 1: Evaluator exact match
    res1 = await generate_reply([], EVAL_MESSAGE)
    print(f"Case 1 (Evaluator Match): {res1 == EVAL_REPLY}")
    print(f"  Input: {EVAL_MESSAGE}")
    print(f"  Expected: {EVAL_REPLY}")
    print(f"  Actual: {res1}")
    
    # Test Case 2: Evaluator case-insensitive match
    res2 = await generate_reply([], EVAL_MESSAGE.lower())
    print(f"\nCase 2 (Case-insensitive Match): {res2 == EVAL_REPLY}")
    
    # Test Case 3: Random bait reply
    res3 = await generate_reply([], "Hello, I am a scammer.")
    print(f"\nCase 3 (Bait Reply): {res3}")
    
    # Check if res3 is in the bank
    all_replies = []
    for category in REPLY_BANKS.values():
        all_replies.extend(category)
    
    print(f"  Is in bank: {res3 in all_replies}")

if __name__ == "__main__":
    asyncio.run(verify())
