#!/usr/bin/env python3
"""
Demo script showing DeepL translation integration
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_translation():
    """Demonstrate translation functionality without requiring API key"""
    
    print("🌐 DeepL Translation Integration Demo")
    print("=" * 50)
    
    # Show supported languages
    from redbot_app import SUPPORTED_LANGUAGES
    
    print("\n📋 Supported Languages:")
    for i, (lang_name, lang_code) in enumerate(SUPPORTED_LANGUAGES.items(), 1):
        print(f"   {i:2d}. {lang_name:<20} ({lang_code})")
    
    # Show example usage
    print("\n💡 Example Usage:")
    print("""
    # In your Streamlit app:
    1. Set DEEPL_API_KEY environment variable
    2. Select language from dropdown in sidebar
    3. Run security assessment
    4. All results automatically translated!
    
    # Programmatic usage:
    from redbot_app import translate_text, translate_finding, translate_plan
    
    # Translate text
    spanish_text = translate_text("Security vulnerability found", "ES")
    
    # Translate finding
    finding = {"snippet": "Email leaked: user@example.com"}
    translated_finding = translate_finding(finding, "FR")
    
    # Translate plan
    plan = {"engineer_plan": {"steps": ["Fix vulnerability"]}}
    translated_plan = translate_plan(plan, "DE")
    """)
    
    # Show UI mockup
    print("\n🖥️  UI Integration:")
    print("""
    ┌─ Sidebar ─────────────────────────┐
    │  🌐 Translation                   │
    │  ┌─────────────────────────────┐  │
    │  │ Translate Results To ▼     │  │
    │  │ English                    │  │
    │  │ Spanish                    │  │
    │  │ French                     │  │
    │  │ German                     │  │
    │  │ Japanese                   │  │
    │  │ Chinese (Simplified)       │  │
    │  │ ...                        │  │
    │  └─────────────────────────────┘  │
    │  🌍 Results will be translated    │
    │     to Spanish                    │
    └───────────────────────────────────┘
    """)
    
    # Show translation flow
    print("\n🔄 Translation Flow:")
    print("""
    1. User selects language from dropdown
    2. Security assessment runs normally
    3. Results displayed in original language
    4. Translation triggered when tab is viewed
    5. Spinner shows during translation
    6. Translated content displayed with language indicator
    """)
    
    # Show error handling
    print("\n⚠️  Error Handling:")
    print("""
    - Missing API key: Shows warning, disables translation
    - Invalid API key: Shows error, falls back to original
    - Network issues: Graceful fallback with warning
    - Translation failures: Returns original text
    """)
    
    print("\n✅ Integration Complete!")
    print("\nTo test with real translations:")
    print("1. Get DeepL API key from https://www.deepl.com/pro-api")
    print("2. Set environment variable: export DEEPL_API_KEY='your-key'")
    print("3. Run: python test_translation.py")

if __name__ == "__main__":
    demo_translation()
