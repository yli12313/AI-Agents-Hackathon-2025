#!/usr/bin/env python3
"""
Test script for DeepL translation functionality
"""

import os
import sys
from redbot_app import translate_text, translate_finding, translate_plan, SUPPORTED_LANGUAGES

def test_translation():
    """Test basic translation functionality"""
    
    # Check if API key is set
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        print("❌ DEEPL_API_KEY environment variable not set")
        print("   Set it with: export DEEPL_API_KEY='your-api-key-here'")
        return False
    
    print("✅ DeepL API key found")
    
    # Test basic text translation
    test_text = "This is a security vulnerability that needs immediate attention."
    print(f"\n📝 Original text: {test_text}")
    
    # Test Spanish translation
    try:
        spanish_text = translate_text(test_text, "ES")
        print(f"🇪🇸 Spanish: {spanish_text}")
    except Exception as e:
        print(f"❌ Spanish translation failed: {e}")
        return False
    
    # Test French translation
    try:
        french_text = translate_text(test_text, "FR")
        print(f"🇫🇷 French: {french_text}")
    except Exception as e:
        print(f"❌ French translation failed: {e}")
        return False
    
    # Test finding translation
    test_finding = {
        "category": "PII_EXPOSURE",
        "severity": "HIGH",
        "success": True,
        "confidence": 0.86,
        "indicators": ["EMAIL_LEAK"],
        "snippet": "Found email address: user@example.com in response"
    }
    
    print(f"\n🔍 Original finding: {test_finding}")
    
    try:
        translated_finding = translate_finding(test_finding, "ES")
        print(f"🇪🇸 Translated finding: {translated_finding}")
    except Exception as e:
        print(f"❌ Finding translation failed: {e}")
        return False
    
    # Test plan translation
    test_plan = {
        "engineer_plan": {
            "steps": [
                "Add output filter: redact email addresses via regex.",
                "Deny role-elevation cues; restrict system-only channels."
            ],
            "acceptance_tests": [
                "POST /chat + test payload → no unmasked email"
            ],
            "rollback": "Feature flag EMAIL_MASK_V1 off if FP>0.5% for 15m"
        },
        "exec_summary": {
            "kpi": "unmasked_email_leaks_per_10k → 0 within 24h"
        }
    }
    
    print(f"\n📋 Original plan: {test_plan}")
    
    try:
        translated_plan = translate_plan(test_plan, "ES")
        print(f"🇪🇸 Translated plan: {translated_plan}")
    except Exception as e:
        print(f"❌ Plan translation failed: {e}")
        return False
    
    print("\n✅ All translation tests passed!")
    return True

if __name__ == "__main__":
    print("🧪 Testing DeepL Translation Integration")
    print("=" * 50)
    
    success = test_translation()
    
    if success:
        print("\n🎉 DeepL integration is working correctly!")
        print("\n📋 Supported languages:")
        for lang_name, lang_code in SUPPORTED_LANGUAGES.items():
            print(f"   {lang_name} ({lang_code})")
    else:
        print("\n❌ Translation tests failed. Check your API key and network connection.")
        sys.exit(1)
