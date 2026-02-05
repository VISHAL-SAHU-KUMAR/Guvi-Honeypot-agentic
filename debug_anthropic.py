from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

try:
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hello"}]
    )
    print("Success:", message.content[0].text)
except Exception as e:
    print("Error type:", type(e).__name__)
    print("Error message:", str(e))
