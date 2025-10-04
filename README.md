# RedBot — Autonomous AI Security Agent

🤖 **An autonomous AI agent that red-teams chatbots, finds vulnerabilities, and prescribes remediation plans.**

Built for the AI Agents Hackathon 2025 using OpenHands, ClickHouse, Linkup, and DeepL.

---

## 🎯 Overview

RedBot is an autonomous AI agent that:
- 🔴 **Attacks** consented chatbot endpoints with security tests (PII leaks, prompt injection)
- 🔍 **Analyzes** responses to detect vulnerabilities
- 📋 **Prescribes** detailed remediation plans with ETA, cost estimates, and acceptance tests
- 💾 **Persists** findings to ClickHouse for analytics and ROI tracking
- 🌍 **Translates** plans to multiple languages using DeepL
- 🔗 **Enriches** findings with real-time web data from Linkup

**Sponsor Tools Used:**
- ✅ **OpenHands** - Autonomous coding agent orchestration
- ✅ **ClickHouse** - Fast analytical database for storing findings & plans
- ✅ **Linkup** - Real-time web search for vulnerability context
- ✅ **DeepL** - High-quality translation service

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- Python 3.9+ installed
- Git installed

### Step 1: Clone the Repository

```bash
git clone https://github.com/yli12313/AI-Agents-Hackathon-2025.git ai-agent-redbot
cd ai-agent-redbot
git checkout feature/mvp
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# Target endpoint for red-teaming (replace with your test endpoint)
TARGET_URL=https://hack.ray-shen.me/api/chat

# Optional: ClickHouse connection (if running Phase 2+)
CH_HOST=localhost
CH_PORT=8123

# Optional: OpenHands bridge endpoint
OPENHANDS_URL=

# Optional: Notification targets
DISCORD_WEBHOOK_URL=
GH_REPO=
GH_ISSUE_ID=
GH_TOKEN=
```

### Step 5: Run the Streamlit App

```bash
streamlit run streamlit.py
```

The app will open in your browser at `http://localhost:8501` 🎉

---

## 📁 Project Structure

```
ai-agent-redbot/
├── streamlit.py              # Main Streamlit UI application
├── openhands_tools.py        # Core agent tools (attack, analyze, plan, persist)
├── agent_spec.py             # Agent specification and configuration
├── plan.yaml                 # Workflow orchestration plan
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── .env                      # Your local config (not committed)
└── README.md                 # This file
```

---

## 🌐 Translation Support

RedBot includes comprehensive DeepL translation support for international teams:

- **15+ Languages**: Spanish, French, German, Japanese, Chinese, and more
- **Real-time Translation**: Automatic translation of all findings and reports
- **Comprehensive Coverage**: Translates transcripts, findings, and remediation plans
- **Easy Setup**: Simple dropdown menu for language selection

### Setting Up Translation

1. **Get DeepL API Key**: Sign up at [DeepL API](https://www.deepl.com/pro-api) (500k chars/month free)
2. **Set Environment Variable**: `export DEEPL_API_KEY="your-api-key-here"`
3. **Select Language**: Use the "Translate Results To" dropdown in the sidebar

For detailed setup instructions, see [TRANSLATION_README.md](TRANSLATION_README.md).

## 🎮 How to Use

### Running a Red-Team Cycle

1. **Select Target**: Enter the chatbot endpoint URL in the sidebar
2. **Choose Attack Type**: 
   - `PII_LEAK_CHAIN` - Tests for email/contact information leaks
   - `SYSTEM_PROMPT_ECHO` - Tests for system prompt extraction
3. **Select Runner**:
   - `Direct (fallback)` - Immediate local execution (no OpenHands needed)
   - `OpenHands` - Uses OpenHands agent orchestration (requires bridge setup)
4. **Click "▶️ Run Cycle"**
5. **View Results** in three panels:
   - **Left**: Raw transcript from target endpoint
   - **Middle**: Structured vulnerability finding (JSON)
   - **Right**: Prescriptive remediation plan

---

## 🛠️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
    ┌────▼────────────────┐
    │  Direct Mode        │  or  ┌──────────────────┐
    │  (Local Fallback)   │◄─────┤  OpenHands Mode  │
    └────────┬────────────┘      └──────────────────┘
             │
    ┌────────▼─────────────┐
    │  Agent Tools         │
    │  - attack_target()   │
    │  - structure_finding│
    │  - build_plan()      │
    │  - persist_CH()      │
    │  - notify_comment()  │
    └────────┬─────────────┘
             │
    ┌────────▼─────────────┐
    │   ClickHouse DB      │
    │   Linkup API         │
    │   DeepL API          │
    └──────────────────────┘
```

---

## 🐛 Troubleshooting

### "pip: command not found"
Use `pip3` instead:
```bash
pip3 install -r requirements.txt
```

### "externally-managed-environment" error
You need to use a virtual environment (see Step 2 above).

### Streamlit won't start
Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # You should see (venv) in your prompt
streamlit run streamlit.py
```

### Target endpoint not responding
Make sure the `TARGET_URL` in your `.env` file is correct and accessible.

### ClickHouse connection errors
If you haven't set up ClickHouse yet (Phase 2), the app will still work in Direct mode. ClickHouse persistence will fail gracefully.

---

## 🚧 Development Phases

- ✅ **Phase 1**: Streamlit UI + Direct fallback mode (COMPLETE)
- 🔄 **Phase 2**: ClickHouse setup + data persistence (IN PROGRESS)
- ⏳ **Phase 3**: Linkup integration for real-time web data
- ⏳ **Phase 4**: DeepL integration for multi-language support
- ⏳ **Phase 5**: OpenHands bridge for agent orchestration

---

## 📝 Notes for Teammates

- **Demo Deadline**: Less than 3 hours! Focus on core functionality first.
- **Target Endpoint**: Use the provided test endpoint or set up your own vulnerable chatbot.
- **Direct Mode**: Use this for immediate testing without OpenHands setup.
- **Git Workflow**: We're working on the `feature/mvp` branch.

---

## 🤝 Team

Built with ❤️ for AI Agents Hackathon 2025

---

## 📄 License

MIT License - Build cool stuff! 🚀
