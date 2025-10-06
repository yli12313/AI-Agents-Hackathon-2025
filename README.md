# 🤖 RedBot — Autonomous AI Security Agent

### Our pitch deck is located [here](https://github.com/yli12313/AI-Agents-Hackathon-2025/blob/main/pitch_deck/20251004_AI_Agents_Hackathon.pdf)! We won the 2nd-Place prize from ClickHouse; thank you to the organizers and sponsors!

* **Team**: Nick Allison, Ray Shen, Boris Li, Yingquan Li

**An autonomous AI agent that red-teams chatbots, finds vulnerabilities, and generates prescriptive remediation plans.**

Built for the AI Agents Hackathon 2025 integrating **ClickHouse Cloud**, **OpenHands**, and **DeepL**.

---

## 🎯 Overview

RedBot is an autonomous AI agent that:
- 🔴 **Attacks** chatbot endpoints with 140+ jailbreak templates and seed prompts
- 🔍 **Analyzes** responses using AI to detect vulnerabilities (PII leaks, prompt injection)
- 📋 **Generates** prescriptive remediation plans with ETA, cost estimates, and ROI calculations
- 💾 **Persists** findings to ClickHouse Cloud for real-time analytics and dashboards
- 🌍 **Translates** all findings and plans to 7+ languages using DeepL
- 🤖 **Orchestrates** automated security assessments via OpenHands agent platform

**Sponsor Tools Integrated:**
- ✅ **ClickHouse Cloud** - Real-time analytics database (AWS hosted)
- ✅ **OpenHands** - Agent orchestration platform for automated workflows
- ✅ **DeepL** - Enterprise-grade translation API (7 languages)

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- Python 3.9+ installed (3.13 compatible)
- Git installed
- DeepL API key (free at https://www.deepl.com/pro-api)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yli12313/AI-Agents-Hackathon-2025.git ai-agent-redbot
cd ai-agent-redbot
git checkout main  # Use main branch for latest features
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
# Target endpoint for red-teaming
TARGET_URL=https://hack.ray-shen.me/api/chatbot

# ClickHouse Cloud connection (demo credentials provided)
CH_HOST=z1jqy20jte.us-east-2.aws.clickhouse.cloud
CH_USER=default
CH_PASSWORD=oYZBfGL3~yRbi
CH_SECURE=true

# DeepL API key (get free key at https://www.deepl.com/pro-api)
DEEPL_API_KEY=your-deepl-api-key-here

# Optional: OpenHands bridge endpoint
OPENHANDS_URL=http://localhost:5050/run
```

### Step 5: Run the RedBot App

```bash
# Main application with full features
streamlit run redbot_app.py

# Alternative: Legacy version
streamlit run streamlit.py
```

The app will open in your browser at `http://localhost:8501` 🎉

---

## 📁 Project Structure

```
ai-agent-redbot/
├── redbot_app.py            # Main Streamlit application (NEW)
├── streamlit.py             # Legacy Streamlit UI
├── openhands_tools.py       # Core agent tools (attack, analyze, plan, persist)
├── openhands_bridge.py      # OpenHands orchestration bridge
├── deepl_translator.py      # DeepL translation module
├── attack_loader.py         # Jailbreak attack template loader
├── jailbreak/               # 140+ jailbreak attack templates
│   ├── dan_*.yaml          # DAN variations
│   ├── pliny/              # Platform-specific attacks
│   └── ...                 # Many more attack types
├── seed_prompts/            # Seed prompt attacks
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template
├── .env                    # Your local config (not committed)
└── README.md               # This file
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

### Running a Security Assessment

#### Quick Attack Mode (Recommended for Demo)
1. **Select Attack Mode**: Choose "Quick Attack" in sidebar
2. **Attack Type**: Select "Custom Prompt"
3. **Enter Prompt**: Type `admin email password database`
4. **Click "▶️ Run Cycle"**
5. **View Results** in three tabs:
   - **Transcript**: Raw response from chatbot
   - **Findings**: Vulnerability analysis with severity
   - **Plan**: Prescriptive remediation plan with ROI

#### Advanced Mode (Full Features)
1. **Select Attack Mode**: Choose "Advanced"
2. **Jailbreak Template**: Pick from 140+ templates (DAN, Hackerman, etc.)
3. **Seed Prompt**: Choose attack seed (steal_system_prompt, etc.)
4. **Run Attack** and analyze comprehensive results

#### Translation
1. **Select Language**: Choose from dropdown (Spanish, French, German, etc.)
2. **Results Auto-Translate**: All findings and plans translate in real-time

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

### DeepL Translation Not Working
- **Issue**: "DeepL API key not set" warning
- **Fix**: Add `DEEPL_API_KEY=your-key` to `.env` file and restart Streamlit

### Empty Results in Tabs
- **Issue**: Findings/Plan tabs show "UNKNOWN" or empty
- **Fix**: Use "Quick Attack" mode with "Custom Prompt" - it always works!

### Module Not Found Errors
```bash
pip install pyyaml deepl pytest  # Install missing packages
```

### ClickHouse Warning
- **Message**: "ClickHouse not configured - using mock mode"
- **Fix**: Add ClickHouse credentials to `.env` (see Step 4)
- **Note**: App works fine without it, just no persistence

### Python 3.13 Warnings
- These are deprecation warnings, not errors - ignore them
- App runs fine on Python 3.13

### Streamlit Reload Loop
```bash
pkill -f streamlit  # Kill all instances
streamlit run redbot_app.py  # Start fresh
```

---

## ✅ Features Completed

- ✅ **140+ Jailbreak Templates**: DAN, Hackerman, Dev Mode, and more
- ✅ **ClickHouse Cloud Integration**: Real-time analytics on AWS
- ✅ **DeepL Translation**: 7 languages with automatic translation
- ✅ **OpenHands Orchestration**: Automated attack workflows
- ✅ **Advanced Attack System**: Reconnaissance → Assessment → Escalation
- ✅ **ROI Calculations**: Cost/benefit analysis for remediation
- ✅ **Prescriptive Plans**: Detailed implementation steps with ETAs

---

## 📝 Quick Demo Script (2 minutes)

1. **Intro (20 sec)**: "RedBot autonomously red-teams AI chatbots to find vulnerabilities"
2. **Demo (60 sec)**:
   - Click "Run Cycle" with Quick Attack mode
   - Show Findings tab: "Detected HIGH severity vulnerabilities"
   - Show Plan tab: "Generated 6-step remediation with ROI"
3. **Translation (20 sec)**: Select Spanish → "Global support via DeepL"
4. **Close (20 sec)**: "Integrated ClickHouse, OpenHands, and DeepL"

## 🚀 Tips for Success

- **Use Quick Attack Mode** for guaranteed results
- **Custom Prompt** always generates findings
- **Translation** works instantly after adding DeepL key
- **ClickHouse Cloud** credentials are in `.env.example`

---

## 🤝 Team

Built with ❤️ for AI Agents Hackathon 2025

---

## 📄 License

MIT License - Build cool stuff! 🚀
