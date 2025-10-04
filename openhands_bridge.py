#!/usr/bin/env python3
"""
Simple OpenHands bridge server for RedBot.
Acts as an orchestration layer between Streamlit and the agent tools.
"""
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Import agent tools
from openhands_tools import attack_target, structure_finding, build_plan, persist_clickhouse

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_cycle():
    """
    Execute a complete red-team cycle.
    Expected input: {"target_url": "...", "attack_type": "..."}
    Returns: {"transcript": "...", "finding": {...}, "plan": {...}}
    """
    try:
        data = request.json
        target_url = data.get('target_url')
        attack_type = data.get('attack_type', 'PII_LEAK_CHAIN')
        
        print(f"🤖 OpenHands Bridge: Running cycle")
        print(f"   Target: {target_url}")
        print(f"   Attack: {attack_type}")
        
        # Step 1: Attack target
        print("   Step 1: Attacking...")
        transcript = attack_target(attack_type)
        
        # Step 2: Analyze response
        print("   Step 2: Analyzing...")
        finding = structure_finding(transcript)
        
        # Step 3: Build plan
        print("   Step 3: Planning...")
        plan = build_plan(finding)
        
        # Step 4: Persist to ClickHouse
        print("   Step 4: Persisting...")
        persist_status = persist_clickhouse(finding, plan)
        
        print(f"   ✅ Cycle complete: {persist_status}")
        
        # Return all data
        return jsonify({
            "transcript": transcript,
            "finding": finding,
            "plan": plan,
            "status": "success"
        })
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "openhands-bridge"})

if __name__ == '__main__':
    print("🚀 OpenHands Bridge Server Starting...")
    print("   Listening on: http://localhost:5050")
    print("   Endpoint: POST /run")
    print()
    app.run(host='0.0.0.0', port=5050, debug=False)
