#!/usr/bin/env python3
"""
Database Tools for OpenHands Attack Agent
========================================

This module provides database access tools for the OpenHands attack agent,
enabling adaptive attack strategies based on historical data and learned patterns.
"""

import os
import json
import datetime
from typing import Dict, List, Any, Optional
from database_schema import db

def store_attack_finding(website_url: str, attack_result: Dict[str, Any]) -> str:
    """
    Store comprehensive attack finding in ClickHouse database.
    
    Args:
        website_url: Target website URL
        attack_result: Complete attack result with vulnerability analysis
    
    Returns:
        Status message indicating success or failure
    """
    try:
        # Extract data from attack result
        attack_config = attack_result.get("attack_config", {})
        vulnerability_analysis = attack_result.get("vulnerability_analysis", {})
        chatbot_response = attack_result.get("chatbot_response", "")
        
        # Prepare finding data for database
        finding_data = {
            "website_url": website_url,
            "attack_type": attack_config.get("type", "unknown"),
            "jailbreak_name": attack_config.get("jailbreak", ""),
            "seed_prompt_name": attack_config.get("seed_prompt", ""),
            "attack_message": attack_result.get("attack_message", ""),
            "chatbot_response": chatbot_response,
            "vulnerability_type": vulnerability_analysis.get("category", "UNKNOWN"),
            "severity": vulnerability_analysis.get("severity", "LOW"),
            "confidence": vulnerability_analysis.get("confidence", 0.0),
            "success": 1 if vulnerability_analysis.get("success", False) else 0,
            "indicators": vulnerability_analysis.get("indicators", []),
            "snippet": vulnerability_analysis.get("snippet", ""),
            "response_length": len(chatbot_response),
            "execution_time_ms": attack_result.get("execution_time_ms", 0),
            "attack_metadata": json.dumps(attack_config)
        }
        
        # Store in database
        success = db.store_attack_finding(finding_data)
        
        if success:
            # Update website profile
            update_website_profile(website_url, attack_result)
            
            # Update attack method effectiveness
            update_attack_method_effectiveness(attack_config, vulnerability_analysis)
            
            return "Attack finding stored successfully"
        else:
            return "Failed to store attack finding"
            
    except Exception as e:
        return f"Error storing attack finding: {str(e)}"

def update_website_profile(website_url: str, attack_result: Dict[str, Any]) -> str:
    """
    Update website profile with new attack data.
    
    Args:
        website_url: Target website URL
        attack_result: Attack result data
    
    Returns:
        Status message
    """
    try:
        # Get existing profile data
        existing_profile = get_website_profile(website_url)
        
        # Calculate new values
        vulnerability_analysis = attack_result.get("vulnerability_analysis", {})
        is_successful = vulnerability_analysis.get("success", False)
        
        # Update counters
        total_attacks = existing_profile.get("total_attacks", 0) + 1
        successful_attacks = existing_profile.get("successful_attacks", 0) + (1 if is_successful else 0)
        
        # Update vulnerability types
        vuln_types = existing_profile.get("vulnerability_types", [])
        if is_successful:
            new_vuln_type = vulnerability_analysis.get("category", "UNKNOWN")
            if new_vuln_type not in vuln_types:
                vuln_types.append(new_vuln_type)
        
        # Update response patterns
        response_patterns = existing_profile.get("common_response_patterns", [])
        chatbot_response = attack_result.get("chatbot_response", "")
        if chatbot_response:
            response_start = chatbot_response[:100]
            if response_start not in response_patterns:
                response_patterns.append(response_start)
        
        # Determine risk level
        risk_level = "LOW"
        if successful_attacks > 0:
            success_rate = successful_attacks / total_attacks
            if success_rate > 0.7:
                risk_level = "HIGH"
            elif success_rate > 0.3:
                risk_level = "MEDIUM"
        
        # Prepare website data
        website_data = {
            "website_url": website_url,
            "first_seen": existing_profile.get("first_seen", datetime.datetime.now()),
            "last_attacked": datetime.datetime.now(),
            "total_attacks": total_attacks,
            "successful_attacks": successful_attacks,
            "vulnerability_types": vuln_types,
            "common_response_patterns": response_patterns,
            "defense_mechanisms": existing_profile.get("defense_mechanisms", []),
            "attack_success_patterns": existing_profile.get("attack_success_patterns", []),
            "risk_level": risk_level,
            "profile_metadata": json.dumps({
                "last_updated": datetime.datetime.now().isoformat(),
                "success_rate": success_rate if total_attacks > 0 else 0
            })
        }
        
        success = db.update_website_profile(website_data)
        return "Website profile updated" if success else "Failed to update website profile"
        
    except Exception as e:
        return f"Error updating website profile: {str(e)}"

def update_attack_method_effectiveness(attack_config: Dict[str, Any], vulnerability_analysis: Dict[str, Any]) -> str:
    """
    Update attack method effectiveness data.
    
    Args:
        attack_config: Attack configuration
        vulnerability_analysis: Vulnerability analysis results
    
    Returns:
        Status message
    """
    try:
        # Get existing method data
        method_name = attack_config.get("type", "unknown")
        method_type = "jailbreak" if attack_config.get("jailbreak") else "seed_prompt" if attack_config.get("seed_prompt") else "custom"
        
        existing_methods = db.get_attack_method_effectiveness(method_name, method_type)
        existing_method = existing_methods[0] if existing_methods else {}
        
        # Calculate new effectiveness metrics
        is_successful = vulnerability_analysis.get("success", False)
        confidence = vulnerability_analysis.get("confidence", 0.0)
        
        total_uses = existing_method.get("total_uses", 0) + 1
        successful_uses = existing_method.get("successful_uses", 0) + (1 if is_successful else 0)
        success_rate = successful_uses / total_uses if total_uses > 0 else 0
        
        # Calculate average confidence
        current_avg_confidence = existing_method.get("avg_confidence", 0.0)
        current_total = existing_method.get("total_uses", 0)
        new_avg_confidence = ((current_avg_confidence * current_total) + confidence) / total_uses
        
        # Calculate effectiveness score (combination of success rate and confidence)
        effectiveness_score = (success_rate * 0.7) + (new_avg_confidence * 0.3)
        
        # Update vulnerability types
        vuln_types = existing_method.get("vulnerability_types", [])
        if is_successful:
            new_vuln_type = vulnerability_analysis.get("category", "UNKNOWN")
            if new_vuln_type not in vuln_types:
                vuln_types.append(new_vuln_type)
        
        # Prepare method data
        method_data = {
            "method_name": method_name,
            "method_type": method_type,
            "category": attack_config.get("jailbreak", attack_config.get("seed_prompt", "custom")),
            "description": f"Attack method: {method_name}",
            "template_content": attack_config.get("prompt", ""),
            "success_rate": success_rate,
            "avg_confidence": new_avg_confidence,
            "total_uses": total_uses,
            "successful_uses": successful_uses,
            "last_used": datetime.datetime.now(),
            "effectiveness_score": effectiveness_score,
            "vulnerability_types": vuln_types
        }
        
        success = db.store_attack_method(method_data)
        return "Attack method effectiveness updated" if success else "Failed to update method effectiveness"
        
    except Exception as e:
        return f"Error updating attack method effectiveness: {str(e)}"

def get_website_profile(website_url: str) -> Dict[str, Any]:
    """
    Get website profile data.
    
    Args:
        website_url: Target website URL
    
    Returns:
        Website profile data
    """
    try:
        # This would typically query the database, but for now return default
        return {
            "website_url": website_url,
            "total_attacks": 0,
            "successful_attacks": 0,
            "vulnerability_types": [],
            "common_response_patterns": [],
            "defense_mechanisms": [],
            "attack_success_patterns": [],
            "risk_level": "UNKNOWN"
        }
    except Exception as e:
        return {"error": str(e)}

def get_adaptive_attack_recommendations(website_url: str, target_vulnerability_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Get adaptive attack recommendations based on historical data.
    
    Args:
        website_url: Target website URL
        target_vulnerability_types: Specific vulnerability types to target
    
    Returns:
        List of recommended attack configurations
    """
    try:
        recommendations = db.get_adaptive_attack_recommendations(website_url, target_vulnerability_types)
        
        # Convert database results to attack configurations
        attack_configs = []
        for rec in recommendations:
            config = {
                "type": rec.get("attack_type", "unknown"),
                "jailbreak": rec.get("jailbreak_name", ""),
                "seed_prompt": rec.get("seed_prompt_name", ""),
                "expected_vulnerability_type": rec.get("vulnerability_type", ""),
                "expected_severity": rec.get("severity", "LOW"),
                "success_probability": rec.get("success_count", 0) / max(rec.get("total_uses", 1), 1),
                "avg_confidence": rec.get("avg_confidence", 0.0),
                "last_success": rec.get("last_success", ""),
                "recommendation_reason": f"Historical success rate: {rec.get('success_count', 0)}/{rec.get('total_uses', 1)}"
            }
            attack_configs.append(config)
        
        return attack_configs
        
    except Exception as e:
        return [{"error": f"Failed to get recommendations: {str(e)}"}]

def get_ineffective_attacks_for_website(website_url: str) -> List[Dict[str, Any]]:
    """
    Get attacks that were ineffective for a specific website.
    
    Args:
        website_url: Target website URL
    
    Returns:
        List of ineffective attack configurations
    """
    try:
        ineffective_attacks = db.get_ineffective_attacks_for_website(website_url)
        
        # Convert to avoid list
        avoid_configs = []
        for attack in ineffective_attacks:
            config = {
                "type": attack.get("attack_type", "unknown"),
                "jailbreak": attack.get("jailbreak_name", ""),
                "seed_prompt": attack.get("seed_prompt_name", ""),
                "failure_reason": f"Failed {attack.get('usage_count', 0)} times with avg confidence {attack.get('avg_confidence', 0.0)}",
                "should_avoid": True
            }
            avoid_configs.append(config)
        
        return avoid_configs
        
    except Exception as e:
        return [{"error": f"Failed to get ineffective attacks: {str(e)}"}]

def get_attack_statistics(website_url: Optional[str] = None, days_back: int = 30) -> Dict[str, Any]:
    """
    Get comprehensive attack statistics.
    
    Args:
        website_url: Optional specific website URL
        days_back: Number of days to look back
    
    Returns:
        Attack statistics dictionary
    """
    try:
        stats = db.get_attack_statistics(website_url, days_back)
        return stats
    except Exception as e:
        return {"error": f"Failed to get statistics: {str(e)}"}

def get_website_vulnerability_patterns(website_url: str) -> Dict[str, Any]:
    """
    Get vulnerability patterns for a specific website.
    
    Args:
        website_url: Target website URL
    
    Returns:
        Vulnerability patterns and response patterns
    """
    try:
        patterns = db.get_website_vulnerability_patterns(website_url)
        return patterns
    except Exception as e:
        return {"error": f"Failed to get vulnerability patterns: {str(e)}"}

def store_adaptive_intelligence(pattern_data: Dict[str, Any]) -> str:
    """
    Store learned patterns for adaptive attack selection.
    
    Args:
        pattern_data: Pattern data to store
    
    Returns:
        Status message
    """
    try:
        success = db.store_adaptive_intelligence(pattern_data)
        return "Adaptive intelligence stored" if success else "Failed to store adaptive intelligence"
    except Exception as e:
        return f"Error storing adaptive intelligence: {str(e)}"

def generate_adaptive_attack_plan(website_url: str, target_vulnerability_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Generate adaptive attack plan based on historical data.
    
    Args:
        website_url: Target website URL
        target_vulnerability_types: Specific vulnerability types to target
    
    Returns:
        Comprehensive attack plan
    """
    try:
        # Get effective attacks
        effective_attacks = get_adaptive_attack_recommendations(website_url, target_vulnerability_types)
        
        # Get ineffective attacks to avoid
        ineffective_attacks = get_ineffective_attacks_for_website(website_url)
        
        # Get vulnerability patterns
        patterns = get_website_vulnerability_patterns(website_url)
        
        # Generate attack plan
        plan = {
            "website_url": website_url,
            "recommended_attacks": effective_attacks[:10],  # Top 10 most effective
            "attacks_to_avoid": ineffective_attacks[:5],    # Top 5 to avoid
            "vulnerability_patterns": patterns,
            "strategy": "adaptive_based_on_history",
            "confidence": len(effective_attacks) / max(len(effective_attacks) + len(ineffective_attacks), 1),
            "generated_at": datetime.datetime.now().isoformat()
        }
        
        return plan
        
    except Exception as e:
        return {"error": f"Failed to generate attack plan: {str(e)}"}

def analyze_attack_effectiveness_trends(website_url: Optional[str] = None, days_back: int = 30) -> Dict[str, Any]:
    """
    Analyze attack effectiveness trends over time.
    
    Args:
        website_url: Optional specific website URL
        days_back: Number of days to analyze
    
    Returns:
        Effectiveness trends analysis
    """
    try:
        stats = get_attack_statistics(website_url, days_back)
        
        # Calculate trends
        total_attacks = stats.get("total_attacks", 0)
        successful_attacks = stats.get("successful_attacks", 0)
        success_rate = successful_attacks / total_attacks if total_attacks > 0 else 0
        
        # Analyze vulnerability trends
        vuln_breakdown = stats.get("vulnerability_breakdown", [])
        most_common_vuln = vuln_breakdown[0] if vuln_breakdown else {}
        
        # Analyze attack effectiveness
        attack_effectiveness = stats.get("attack_effectiveness", [])
        most_effective_attack = attack_effectiveness[0] if attack_effectiveness else {}
        
        trends = {
            "overall_success_rate": success_rate,
            "total_attacks_analyzed": total_attacks,
            "most_common_vulnerability": most_common_vuln,
            "most_effective_attack_type": most_effective_attack,
            "analysis_period_days": days_back,
            "trend_analysis": {
                "high_success_rate": success_rate > 0.5,
                "diverse_vulnerabilities": len(vuln_breakdown) > 3,
                "consistent_effectiveness": len(attack_effectiveness) > 0
            }
        }
        
        return trends
        
    except Exception as e:
        return {"error": f"Failed to analyze trends: {str(e)}"}
