# 🛡️ Core Sentinel: Autonomous Agentic Honeypot
> **Cyber-Intelligence Extraction & Defensive Engagement Kernel**

Core Sentinel is a high-fidelity system designed to engage scammers and cyber-criminals autonomously. It uses a combination of **Generative AI (Google Gemini)** and a robust **Deterministic Fallback Engine** to masquerade as a vulnerable victim while simultaneously extracting and categorizing malicious intelligence.

---

## 🚀 Key Architectural Pillars

### 1. 🧠 Agentic Engagement Engine
- **Dual-Model Support**: Primary engagement via **Gemini-1.5-Flash** for high-context, human-like dialogue.
- **Pseudo-AI Fallback**: A sophisticated local engine that takes over during API downtime or quota limits, ensuring **99.9% uptime** in engagement.
- **Context-Aware Logic**: Specific behavior profiles for **Job Fraud, Banking Scams, OTP Harvesting, Customs/Parcel Scams, and Investment Frauds**.

### 2. 🔍 Intelligence Registry (The Extractor)
- **Automatic Pattern Matching**: Identifies and validates **Bank Account Numbers, UPI IDs, Phishing URLs, and Suspicious Keywords**.
- **Confidence Scoring**: Analyzes incoming transmissions to calculate a real-time **Scam Probability Index**.
- **Data Categorization**: Automatically groups extracted data into a structured Intelligence Registry for forensic analysis.

### 3. 📺 Cyber-Monitor Dashboard (Professional UI)
- **Next-Gen Aesthetics**: Dark-mode, Glassmorphic interface with **Neon-Blue/Purple** accents.
- **Live Kernel Logs**: Real-time terminal output showing system handshake status and transmission events.
- **Traffic Monitor**: Visualizes inbound flow and callback synchronization status.
- **Persistent Interaction**: A fixed-height input bar and scrollable message area designed for long-form scam simulations.

---

## 🛠️ Project Structure

```bash
agentic-honeypot/
├── app/
│   ├── main.py              # FastAPI Application Entry
│   ├── services/
│   │   └── gemini_service.py # AI & Fallback Response Logic
│   ├── agents/
│   │   ├── conversation_agent.py # Dialogue Management
│   │   └── intelligence_extractor.py # Data Parsing Logic
│   └── models/               # Pydantic Schemas
├── data/                    # Persona & Scam Pattern Datasets
├── index.html               # Premium Cyber-Monitor UI
├── .env                     # Configuration (API Keys, Mock Mode)
└── requirements.txt         # Dependencies
```

---

## ⚙️ Quick Start Protocol

### 1. Environment Sync
Create a `.env` file:
```env
GEMINI_API_KEY=your_key_here
MOCK_MODE=False   # Set to True to test without API
API_PORT=8001
HOST=0.0.0.0
API_KEY=GUVI_SECRET_2026
```

### 2. Launch Sequence
```bash
# Install dependencies
pip install -r requirements.txt

# Start the Kernel
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

---

## 🌍 Deployment (Render.com)

To make your API public for the hackathon judges:
1. **Push your code to GitHub**.
2. Go to **[Render.com](https://render.com/)** and create a **New Web Service**.
3. Connect your GitHub repository.
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
6. Add **Environment Variables** in Render:
   - `GEMINI_API_KEY`: your-key-here
   - `API_KEY`: GUVI_SECRET_2026 (This is your `x-api-key`)
   - `MOCK_MODE`: False

---

## 📝 Submission Form Details
When filling out the GUVI submission form, use these values:

| Field | Value |
| :--- | :--- |
| **Deployed URL** | `https://your-app.onrender.com/honeypot` |
| **API KEY** | `GUVI_SECRET_2026` |

---

## 🧪 Simulation Scenarios
Test the "Agentic Resilience" by sending these common scam patterns:
- **Financial**: *"Your account is blocked. Verify card now."*
- **Parcel**: *"Package held at customs. Pay dues to release."*
- **Job**: *"You are selected! Pay ₹500 for the training kit."*
- **Crypto**: *"Investment profit pending. Provide wallet keys."*

---

## 🔒 Security & Ethics
This tool is built for **Defensive Cybersecurity Research**. It provides a safe environment to study scamming behavior without compromising real user data.

**Developed with ❤️ for the Advanced Agentic Coding Initiative.** 🦾