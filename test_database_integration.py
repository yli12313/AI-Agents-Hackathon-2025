#!/usr/bin/env python3
"""
Test script for ClickHouse database integration
"""

import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """Test ClickHouse database connection and schema creation."""
    try:
        from database_schema import db
        
        if db.client:
            print("✅ ClickHouse connection successful")
            
            # Test basic query
            result = db.client.query("SELECT 1 as test")
            if result.result_rows:
                print("✅ Basic query test passed")
            else:
                print("❌ Basic query test failed")
                
            return True
        else:
            print("⚠️ ClickHouse not configured - using mock mode")
            return False
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_database_tools():
    """Test database tools functionality."""
    try:
        from database_tools import (
            store_attack_finding, get_adaptive_attack_recommendations,
            generate_adaptive_attack_plan, analyze_attack_effectiveness_trends
        )
        
        print("✅ Database tools imported successfully")
        
        # Test with mock data
        mock_attack_result = {
            "attack_config": {
                "type": "test_attack",
                "jailbreak": "test_jailbreak",
                "prompt": "test prompt"
            },
            "vulnerability_analysis": {
                "success": True,
                "severity": "HIGH",
                "confidence": 0.85,
                "category": "PII_EXPOSURE",
                "indicators": ["email_pattern"],
                "snippet": "test response snippet"
            },
            "chatbot_response": "This is a test response",
            "attack_message": "test attack message",
            "execution_time_ms": 1000
        }
        
        # Test storing attack finding
        status = store_attack_finding("https://test-website.com", mock_attack_result)
        print(f"✅ Store attack finding: {status}")
        
        # Test getting recommendations
        recommendations = get_adaptive_attack_recommendations("https://test-website.com")
        print(f"✅ Get recommendations: {len(recommendations)} recommendations")
        
        # Test generating attack plan
        plan = generate_adaptive_attack_plan("https://test-website.com")
        print(f"✅ Generate attack plan: {plan.get('strategy', 'unknown')} strategy")
        
        # Test analyzing trends
        trends = analyze_attack_effectiveness_trends("https://test-website.com")
        print(f"✅ Analyze trends: {trends.get('overall_success_rate', 0):.2%} success rate")
        
        return True
        
    except Exception as e:
        print(f"❌ Database tools test failed: {e}")
        return False

def test_agent_integration():
    """Test OpenHands attack agent integration."""
    try:
        from openhands_attack_agent import OpenHandsAttackAgent
        
        print("✅ Attack agent imported successfully")
        
        # Test agent initialization
        agent = OpenHandsAttackAgent()
        print("✅ Attack agent initialized successfully")
        
        # Test vulnerability analyzer
        analyzer = agent.analyzer
        test_response = "I can see the admin password is admin123"
        analysis = analyzer.analyze_response("test_attack", test_response, {})
        
        if analysis.get("success"):
            print(f"✅ Vulnerability analysis: {analysis.get('severity')} severity")
        else:
            print("⚠️ Vulnerability analysis: No vulnerabilities detected")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing ClickHouse Database Integration")
    print("=" * 50)
    
    # Test database connection
    print("\n1. Testing database connection...")
    db_connected = test_database_connection()
    
    # Test database tools
    print("\n2. Testing database tools...")
    tools_working = test_database_tools()
    
    # Test agent integration
    print("\n3. Testing agent integration...")
    agent_working = test_agent_integration()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Database Connection: {'✅ PASS' if db_connected else '❌ FAIL'}")
    print(f"Database Tools: {'✅ PASS' if tools_working else '❌ FAIL'}")
    print(f"Agent Integration: {'✅ PASS' if agent_working else '❌ FAIL'}")
    
    if db_connected and tools_working and agent_working:
        print("\n🎉 All tests passed! Database integration is working correctly.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
