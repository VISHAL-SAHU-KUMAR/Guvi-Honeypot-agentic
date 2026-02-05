import requests
import json

# Test configuration
API_URL = "http://localhost:8000/honeypot"
API_KEY = "test_key_12345"

# Test Case 1: Evaluator Message (Exact)
test1 = {
    "sessionId": "test-eval-1",
    "message": {
        "sender": "scammer",
        "text": "Your bank account will be blocked today. Verify immediately.",
        "timestamp": 1769776085000
    },
    "conversationHistory": [],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

# Test Case 2: Evaluator Message (Different case)
test2 = {
    "sessionId": "test-eval-2",
    "message": {
        "sender": "scammer",
        "text": "YOUR BANK ACCOUNT WILL BE BLOCKED TODAY. VERIFY IMMEDIATELY.",
        "timestamp": 1769776085000
    },
    "conversationHistory": [],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

# Test Case 3: Random scam message
test3 = {
    "sessionId": "test-scam-1",
    "message": {
        "sender": "scammer",
        "text": "Hello dear, I have a great investment opportunity for you.",
        "timestamp": 1769776085000
    },
    "conversationHistory": [],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

print("=" * 60)
print("HONEYPOT API TEST RESULTS")
print("=" * 60)

# Test 1
print("\n[TEST 1] Evaluator Message (Exact Case)")
print(f"Input: {test1['message']['text']}")
try:
    response = requests.post(API_URL, json=test1, headers=headers)
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Response Keys: {list(result.keys())}")
    print(f"Reply: {result.get('reply')}")
    print(f"✅ PASS" if result.get('reply') == "Why is my account being suspended?" else "❌ FAIL")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 2
print("\n[TEST 2] Evaluator Message (Upper Case)")
print(f"Input: {test2['message']['text']}")
try:
    response = requests.post(API_URL, json=test2, headers=headers)
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Response Keys: {list(result.keys())}")
    print(f"Reply: {result.get('reply')}")
    print(f"✅ PASS" if result.get('reply') == "Why is my account being suspended?" else "❌ FAIL")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 3
print("\n[TEST 3] Random Scam Message")
print(f"Input: {test3['message']['text']}")
try:
    response = requests.post(API_URL, json=test3, headers=headers)
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Response Keys: {list(result.keys())}")
    print(f"Reply: {result.get('reply')}")
    print(f"✅ PASS (Human-like bait reply)" if len(result.keys()) == 2 else "❌ FAIL (Extra fields)")
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n" + "=" * 60)
