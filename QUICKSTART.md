# 🚀 RedBot Quick Start Guide

**Get RedBot running in under 2 minutes!**

## The Fastest Way

```bash
# 1. Run the setup script
./setup.sh

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Start the app
streamlit run streamlit.py
```

That's it! Open your browser at `http://localhost:8501` 🎉

---

## Optional: ClickHouse Database

If you want to test ClickHouse persistence:

```bash
# Make sure Docker Desktop is running, then:
docker-compose up -d

# Check it's running:
docker ps

# View logs:
docker-compose logs clickhouse
```

The app works perfectly fine WITHOUT ClickHouse - it will use in-memory storage for the demo.

---

## Demo Flow (3 minutes)

1. **Open the app** at http://localhost:8501
2. **Configure target** in sidebar (default is fine)
3. **Click "Run Cycle"** - watch the agent work!
4. **Show results** in 3 panels:
   - Transcript (raw data from target)
   - Finding (structured vulnerability)
   - Plan (prescriptive remediation)
5. **Explain autonomy**: Agent independently attacks, analyzes, and prescribes fixes
6. **Show ROI metrics**: ETA, cost, risk reduction per hour

---

## Troubleshooting

**Streamlit won't start?**
```bash
source venv/bin/activate  # Make sure venv is active
```

**Target endpoint errors?**
- Check `.env` file has correct `TARGET_URL`
- Default target should work: `https://hack.ray-shen.me/api/chat`

**Docker not running?**
- Open Docker Desktop app
- Wait for it to fully start (whale icon in menu bar)
- Then run `docker-compose up -d`

---

## File Structure

```
ai-agent-redbot/
├── streamlit.py           # 🎨 Main UI (run this!)
├── openhands_tools.py     # 🔧 Agent tools
├── agent_spec.py          # 📋 Agent configuration  
├── plan.yaml              # 📊 Workflow orchestration
├── requirements.txt       # 📦 Python dependencies
├── setup.sh              # ⚡ One-command setup
├── docker-compose.yml     # 🐳 ClickHouse container
├── docker/
│   └── schema.sql        # 🗄️ Database schema
├── .env                   # ⚙️ Your config (local)
├── .env.example          # ⚙️ Config template
└── README.md             # 📖 Full documentation
```

---

## Next Steps After Demo

- Add Linkup integration for real-time web enrichment
- Add DeepL for multi-language support
- Connect OpenHands for full agent orchestration
- Deploy to cloud for continuous monitoring

**Good luck with the demo!** 🚀
