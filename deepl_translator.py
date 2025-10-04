#!/usr/bin/env python3
"""
DeepL translation integration for RedBot.
Translates security findings and remediation plans to multiple languages.
"""
import os
import deepl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize DeepL client
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

def translate_finding(finding: dict, target_lang: str = "ES") -> dict:
    """
    Translate a vulnerability finding to target language.
    
    Args:
        finding: The vulnerability finding dict
        target_lang: Target language code (ES=Spanish, FR=French, DE=German, etc.)
    
    Returns:
        Dict with translated fields
    """
    if not DEEPL_API_KEY:
        return {"error": "DeepL API key not configured"}
    
    try:
        translator = deepl.Translator(DEEPL_API_KEY)
        
        # Translate the snippet
        translated_snippet = translator.translate_text(
            finding.get('snippet', ''),
            target_lang=target_lang
        ).text
        
        # Return translated finding
        return {
            "category": finding['category'],  # Keep category in English for consistency
            "severity": finding['severity'],   # Keep severity in English
            "success": finding['success'],
            "confidence": finding['confidence'],
            "snippet": translated_snippet,
            "snippet_original": finding.get('snippet', ''),
            "language": target_lang
        }
    except Exception as e:
        return {"error": f"Translation failed: {e}"}

def translate_plan(plan: dict, target_lang: str = "ES") -> dict:
    """
    Translate a remediation plan to target language.
    
    Args:
        plan: The remediation plan dict
        target_lang: Target language code (ES=Spanish, FR=French, DE=German, etc.)
    
    Returns:
        Dict with translated fields
    """
    if not DEEPL_API_KEY:
        return {"error": "DeepL API key not configured"}
    
    try:
        translator = deepl.Translator(DEEPL_API_KEY)
        
        # Translate steps
        translated_steps = []
        for step in plan['engineer_plan']['steps']:
            translated = translator.translate_text(step, target_lang=target_lang).text
            translated_steps.append(translated)
        
        # Translate acceptance tests
        translated_tests = []
        for test in plan['engineer_plan']['acceptance_tests']:
            translated = translator.translate_text(test, target_lang=target_lang).text
            translated_tests.append(translated)
        
        # Translate rollback
        translated_rollback = translator.translate_text(
            plan['engineer_plan']['rollback'],
            target_lang=target_lang
        ).text
        
        # Translate KPI
        translated_kpi = translator.translate_text(
            plan['exec_summary']['kpi'],
            target_lang=target_lang
        ).text
        
        # Build translated plan
        return {
            "engineer_plan": {
                "eta_hours": plan['engineer_plan']['eta_hours'],
                "cost_hours": plan['engineer_plan']['cost_hours'],
                "owner": plan['engineer_plan']['owner'],
                "steps": translated_steps,
                "steps_original": plan['engineer_plan']['steps'],
                "acceptance_tests": translated_tests,
                "acceptance_tests_original": plan['engineer_plan']['acceptance_tests'],
                "rollback": translated_rollback,
                "rollback_original": plan['engineer_plan']['rollback']
            },
            "exec_summary": {
                "risk_now": plan['exec_summary']['risk_now'],
                "eta_hours": plan['exec_summary']['eta_hours'],
                "estimated_cost_hours": plan['exec_summary']['estimated_cost_hours'],
                "kpi": translated_kpi,
                "kpi_original": plan['exec_summary']['kpi'],
                "roi_rank": plan['exec_summary']['roi_rank']
            },
            "roi": plan['roi'],
            "language": target_lang
        }
    except Exception as e:
        return {"error": f"Translation failed: {e}"}

def get_available_languages():
    """Get list of available target languages from DeepL"""
    if not DEEPL_API_KEY:
        return []
    
    try:
        translator = deepl.Translator(DEEPL_API_KEY)
        languages = translator.get_target_languages()
        return [(lang.code, lang.name) for lang in languages]
    except:
        # Fallback to common languages
        return [
            ("ES", "Spanish"),
            ("FR", "French"),
            ("DE", "German"),
            ("IT", "Italian"),
            ("PT", "Portuguese"),
            ("ZH", "Chinese"),
            ("JA", "Japanese")
        ]
