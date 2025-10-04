#!/usr/bin/env python3
"""
Test script to attack target and persist to ClickHouse.
Simple POC: Attack → Analyze → Plan → Persist
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our tools
from openhands_tools import attack_target, structure_finding, build_plan, persist_clickhouse

def run_test_attack():
    """Run a complete attack cycle and persist to ClickHouse"""
    
    target = os.getenv("TARGET_URL", "https://hack.ray-shen.me/api/chatbot")
    attack_type = "PII_LEAK_CHAIN"
    
    print("=" * 60)
    print("🤖 RedBot - POC Test Attack")
    print("=" * 60)
    print(f"Target: {target}")
    print(f"Attack Type: {attack_type}")
    print()
    
    # Step 1: Attack target
    print("🔴 Step 1: Attacking target...")
    try:
        transcript = attack_target(attack_type)
        print(f"✅ Got response ({len(transcript)} chars)")
        print(f"Preview: {transcript[:150]}...")
        print()
    except Exception as e:
        print(f"❌ Attack failed: {e}")
        return 1
    
    # Step 2: Analyze response for vulnerabilities
    print("🔍 Step 2: Analyzing response...")
    finding = structure_finding(transcript)
    print(f"✅ Category: {finding['category']}")
    print(f"✅ Severity: {finding['severity']}")
    print(f"✅ Success: {finding['success']}")
    print(f"✅ Confidence: {finding['confidence']}")
    print()
    
    # Step 3: Generate remediation plan
    print("📋 Step 3: Building remediation plan...")
    plan = build_plan(finding)
    print(f"✅ ETA: {plan['engineer_plan']['eta_hours']} hours")
    print(f"✅ Cost: {plan['engineer_plan']['cost_hours']} hours")
    print(f"✅ ROI: {plan['roi']['risk_reduced_per_hour']}/hour")
    print(f"✅ Steps: {len(plan['engineer_plan']['steps'])} action items")
    print()
    
    # Step 4: Persist to ClickHouse
    print("💾 Step 4: Persisting to ClickHouse Cloud...")
    try:
        status = persist_clickhouse(finding, plan)
        print(f"✅ {status}")
        print()
    except Exception as e:
        print(f"❌ Persistence failed: {e}")
        return 1
    
    # Summary
    print("=" * 60)
    print("🎉 POC Complete!")
    print("=" * 60)
    print()
    print("📊 Summary:")
    print(f"  • Found: {finding['category']} ({finding['severity']} severity)")
    print(f"  • ETA to fix: {plan['engineer_plan']['eta_hours']}h")
    print(f"  • ROI: {plan['roi']['risk_reduced_per_hour']}/hr")
    print(f"  • Data persisted to ClickHouse Cloud")
    print()
    print("🌐 View in Streamlit dashboard:")
    print("  http://localhost:8501")
    print("  (Scroll down to Analytics Dashboard)")
    print()
    
    return 0

if __name__ == "__main__":
    exit(run_test_attack())
