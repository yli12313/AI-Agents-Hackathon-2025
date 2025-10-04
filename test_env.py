#!/usr/bin/env python3
"""
Test script to verify environment variable loading
"""

import os

def test_env_loading():
    """Test if DEEPL_API_KEY is being loaded correctly"""
    
    print("🔍 Environment Variable Test")
    print("=" * 40)
    
    # Check if environment variable is set
    api_key = os.getenv("DEEPL_API_KEY")
    
    print(f"DEEPL_API_KEY from os.getenv(): {api_key}")
    print(f"Type: {type(api_key)}")
    print(f"Length: {len(api_key) if api_key else 0}")
    
    if api_key:
        print("✅ DEEPL_API_KEY is set correctly")
        print(f"   Key: {api_key[:10]}...{api_key[-10:]}")
    else:
        print("❌ DEEPL_API_KEY is not set")
        
        # Check all environment variables that contain DEEPL
        print("\n🔍 All environment variables containing 'DEEPL':")
        for key, value in os.environ.items():
            if 'DEEPL' in key.upper():
                print(f"   {key}: {value}")
    
    # Test the same logic as in redbot_app.py
    if api_key:
        print("\n✅ Translation would be enabled")
        try:
            import deepl
            translator = deepl.Translator(api_key)
            print("✅ DeepL translator created successfully")
        except Exception as e:
            print(f"❌ DeepL translator creation failed: {e}")
    else:
        print("\n❌ Translation would be disabled")

if __name__ == "__main__":
    test_env_loading()
