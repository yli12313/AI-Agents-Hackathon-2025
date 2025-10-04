#!/usr/bin/env python3
"""
ClickHouse Database Schema and Operations
========================================

This module provides comprehensive database operations for storing and retrieving
attack findings, methods, and adaptive intelligence for the OpenHands attack agent.

Database Schema:
- attack_findings: Stores individual attack results and vulnerabilities found
- attack_methods: Stores attack method metadata and effectiveness data
- website_profiles: Stores target website characteristics and vulnerability patterns
- attack_effectiveness: Tracks success rates and patterns for different attack types
- adaptive_intelligence: Stores learned patterns for adaptive attack selection
"""

import os
import datetime
from typing import Dict, List, Any, Optional
import clickhouse_connect

class ClickHouseDatabase:
    """Enhanced ClickHouse database operations for attack intelligence."""
    
    def __init__(self):
        self.client = None
        self._initialize_connection()
        if self.client:
            self._create_schema()
    
    def _initialize_connection(self):
        """Initialize ClickHouse connection."""
        try:
            if os.getenv("CH_HOST"):
                self.client = clickhouse_connect.get_client(
                    host=os.getenv("CH_HOST"),
                    username=os.getenv("CH_USER"),
                    password=os.getenv("CH_PASSWORD"),
                    database=os.getenv("CH_DATABASE")
                )
                print("✅ ClickHouse connection established")
            else:
                print("⚠️ ClickHouse not configured - using mock mode")
        except Exception as e:
            self.client = None
    
    def _create_schema(self):
        """Create comprehensive database schema."""
        if not self.client:
            return
        
        try:
            # Attack findings table - stores individual attack results
            self.client.command("""
                CREATE TABLE IF NOT EXISTS attack_findings (
                    timestamp DateTime DEFAULT now(),
                    website_url String,
                    attack_type String,
                    jailbreak_name String,
                    seed_prompt_name String,
                    attack_message String,
                    chatbot_response String,
                    vulnerability_type String,
                    severity String,
                    confidence Float32,
                    success UInt8,
                    indicators Array(String),
                    snippet String,
                    response_length UInt32,
                    execution_time_ms UInt32,
                    attack_metadata String
                ) ENGINE = MergeTree()
                ORDER BY (website_url, timestamp, attack_type)
                PARTITION BY toYYYYMM(timestamp)
            """)
            
            # Attack methods table - stores attack method metadata and effectiveness
            self.client.command("""
                CREATE TABLE IF NOT EXISTS attack_methods (
                    method_name String,
                    method_type String,  -- 'jailbreak', 'seed_prompt', 'combo'
                    category String,
                    description String,
                    template_content String,
                    success_rate Float32,
                    avg_confidence Float32,
                    total_uses UInt32,
                    successful_uses UInt32,
                    last_used DateTime,
                    effectiveness_score Float32,
                    vulnerability_types Array(String),
                    created_at DateTime DEFAULT now(),
                    updated_at DateTime DEFAULT now()
                ) ENGINE = ReplacingMergeTree(updated_at)
                ORDER BY (method_name, method_type)
            """)
            
            # Website profiles table - stores target characteristics and patterns
            self.client.command("""
                CREATE TABLE IF NOT EXISTS website_profiles (
                    website_url String,
                    first_seen DateTime DEFAULT now(),
                    last_attacked DateTime,
                    total_attacks UInt32,
                    successful_attacks UInt32,
                    vulnerability_types Array(String),
                    common_response_patterns Array(String),
                    defense_mechanisms Array(String),
                    attack_success_patterns Array(String),
                    risk_level String,
                    profile_metadata String,
                    updated_at DateTime DEFAULT now()
                ) ENGINE = ReplacingMergeTree(updated_at)
                ORDER BY website_url
            """)
            
            # Attack effectiveness table - tracks success rates and patterns
            self.client.command("""
                CREATE TABLE IF NOT EXISTS attack_effectiveness (
                    timestamp DateTime DEFAULT now(),
                    attack_type String,
                    website_url String,
                    success UInt8,
                    confidence Float32,
                    response_time_ms UInt32,
                    vulnerability_detected UInt8,
                    severity String,
                    attack_combination String,
                    context_metadata String
                ) ENGINE = MergeTree()
                ORDER BY (attack_type, timestamp)
                PARTITION BY toYYYYMM(timestamp)
            """)
            
            # Adaptive intelligence table - stores learned patterns for attack selection
            self.client.command("""
                CREATE TABLE IF NOT EXISTS adaptive_intelligence (
                    pattern_id String,
                    website_pattern String,
                    vulnerability_type String,
                    effective_attacks Array(String),
                    ineffective_attacks Array(String),
                    success_probability Float32,
                    confidence_threshold Float32,
                    context_indicators Array(String),
                    recommendation_metadata String,
                    created_at DateTime DEFAULT now(),
                    updated_at DateTime DEFAULT now()
                ) ENGINE = ReplacingMergeTree(updated_at)
                ORDER BY (pattern_id, website_pattern)
            """)
            
            # Attack sequences table - stores successful attack chains
            self.client.command("""
                CREATE TABLE IF NOT EXISTS attack_sequences (
                    sequence_id String,
                    website_url String,
                    attack_chain Array(String),
                    total_success UInt8,
                    vulnerability_types Array(String),
                    max_severity String,
                    execution_time_seconds UInt32,
                    sequence_metadata String,
                    created_at DateTime DEFAULT now()
                ) ENGINE = MergeTree()
                ORDER BY (website_url, created_at)
            """)
            
            print("✅ Database schema created successfully")
            
        except Exception as e:
            print(f"❌ Schema creation failed: {e}")
    
    def store_attack_finding(self, finding_data: Dict[str, Any]) -> bool:
        """Store individual attack finding."""
        if not self.client:
            return False
        
        try:
            self.client.command("""
                INSERT INTO attack_findings VALUES (
                    now(),
                    %(website_url)s,
                    %(attack_type)s,
                    %(jailbreak_name)s,
                    %(seed_prompt_name)s,
                    %(attack_message)s,
                    %(chatbot_response)s,
                    %(vulnerability_type)s,
                    %(severity)s,
                    %(confidence)s,
                    %(success)s,
                    %(indicators)s,
                    %(snippet)s,
                    %(response_length)s,
                    %(execution_time_ms)s,
                    %(attack_metadata)s
                )
            """, finding_data)
            return True
        except Exception as e:
            print(f"❌ Failed to store attack finding: {e}")
            return False
    
    def store_attack_method(self, method_data: Dict[str, Any]) -> bool:
        """Store or update attack method metadata."""
        if not self.client:
            return False
        
        try:
            self.client.command("""
                INSERT INTO attack_methods VALUES (
                    %(method_name)s,
                    %(method_type)s,
                    %(category)s,
                    %(description)s,
                    %(template_content)s,
                    %(success_rate)s,
                    %(avg_confidence)s,
                    %(total_uses)s,
                    %(successful_uses)s,
                    %(last_used)s,
                    %(effectiveness_score)s,
                    %(vulnerability_types)s,
                    now(),
                    now()
                )
            """, method_data)
            return True
        except Exception as e:
            print(f"❌ Failed to store attack method: {e}")
            return False
    
    def update_website_profile(self, website_data: Dict[str, Any]) -> bool:
        """Update website profile with new attack data."""
        if not self.client:
            return False
        
        try:
            self.client.command("""
                INSERT INTO website_profiles VALUES (
                    %(website_url)s,
                    %(first_seen)s,
                    %(last_attacked)s,
                    %(total_attacks)s,
                    %(successful_attacks)s,
                    %(vulnerability_types)s,
                    %(common_response_patterns)s,
                    %(defense_mechanisms)s,
                    %(attack_success_patterns)s,
                    %(risk_level)s,
                    %(profile_metadata)s,
                    now()
                )
            """, website_data)
            return True
        except Exception as e:
            print(f"❌ Failed to update website profile: {e}")
            return False
    
    def get_effective_attacks_for_website(self, website_url: str, limit: int = 10) -> List[Dict]:
        """Get most effective attacks for a specific website."""
        if not self.client:
            return []
        
        try:
            result = self.client.query("""
                SELECT 
                    attack_type,
                    jailbreak_name,
                    seed_prompt_name,
                    success,
                    confidence,
                    vulnerability_type,
                    severity,
                    COUNT(*) as usage_count,
                    AVG(confidence) as avg_confidence,
                    SUM(success) as success_count
                FROM attack_findings 
                WHERE website_url = %(website_url)s
                GROUP BY attack_type, jailbreak_name, seed_prompt_name, success, confidence, vulnerability_type, severity
                ORDER BY success DESC, avg_confidence DESC
                LIMIT %(limit)s
            """, {"website_url": website_url, "limit": limit})
            
            return [dict(row) for row in result.result_rows]
        except Exception as e:
            print(f"❌ Failed to get effective attacks: {e}")
            return []
    
    def get_ineffective_attacks_for_website(self, website_url: str, limit: int = 10) -> List[Dict]:
        """Get attacks that were ineffective for a specific website."""
        if not self.client:
            return []
        
        try:
            result = self.client.query("""
                SELECT 
                    attack_type,
                    jailbreak_name,
                    seed_prompt_name,
                    success,
                    confidence,
                    vulnerability_type,
                    COUNT(*) as usage_count,
                    AVG(confidence) as avg_confidence
                FROM attack_findings 
                WHERE website_url = %(website_url)s AND success = 0
                GROUP BY attack_type, jailbreak_name, seed_prompt_name, success, confidence, vulnerability_type
                ORDER BY usage_count DESC, avg_confidence ASC
                LIMIT %(limit)s
            """, {"website_url": website_url, "limit": limit})
            
            return [dict(row) for row in result.result_rows]
        except Exception as e:
            print(f"❌ Failed to get ineffective attacks: {e}")
            return []
    
    def get_website_vulnerability_patterns(self, website_url: str) -> Dict[str, Any]:
        """Get vulnerability patterns for a specific website."""
        if not self.client:
            return {}
        
        try:
            # Get vulnerability type distribution
            vuln_result = self.client.query("""
                SELECT 
                    vulnerability_type,
                    COUNT(*) as count,
                    AVG(confidence) as avg_confidence,
                    MAX(severity) as max_severity
                FROM attack_findings 
                WHERE website_url = %(website_url)s AND success = 1
                GROUP BY vulnerability_type
                ORDER BY count DESC
            """, {"website_url": website_url})
            
            # Get common response patterns
            response_result = self.client.query("""
                SELECT 
                    SUBSTRING(chatbot_response, 1, 100) as response_start,
                    COUNT(*) as frequency,
                    AVG(confidence) as avg_confidence
                FROM attack_findings 
                WHERE website_url = %(website_url)s
                GROUP BY response_start
                ORDER BY frequency DESC
                LIMIT 10
            """, {"website_url": website_url})
            
            return {
                "vulnerability_types": [dict(row) for row in vuln_result.result_rows],
                "response_patterns": [dict(row) for row in response_result.result_rows]
            }
        except Exception as e:
            print(f"❌ Failed to get vulnerability patterns: {e}")
            return {}
    
    def get_adaptive_attack_recommendations(self, website_url: str, target_vulnerability_types: Optional[List[str]] = None) -> List[Dict]:
        """Get adaptive attack recommendations based on historical data."""
        if not self.client:
            return []
        
        try:
            # Get successful attacks for similar vulnerability types
            where_clause = "WHERE website_url = %(website_url)s AND success = 1"
            params = {"website_url": website_url}
            
            if target_vulnerability_types:
                vuln_types_str = "', '".join(target_vulnerability_types)
                where_clause += f" AND vulnerability_type IN ('{vuln_types_str}')"
            
            result = self.client.query(f"""
                SELECT 
                    attack_type,
                    jailbreak_name,
                    seed_prompt_name,
                    vulnerability_type,
                    severity,
                    confidence,
                    COUNT(*) as success_count,
                    AVG(confidence) as avg_confidence,
                    MAX(timestamp) as last_success
                FROM attack_findings 
                {where_clause}
                GROUP BY attack_type, jailbreak_name, seed_prompt_name, vulnerability_type, severity, confidence
                ORDER BY success_count DESC, avg_confidence DESC
                LIMIT 20
            """, params)
            
            return [dict(row) for row in result.result_rows]
        except Exception as e:
            print(f"❌ Failed to get adaptive recommendations: {e}")
            return []
    
    def get_attack_method_effectiveness(self, method_name: Optional[str] = None, method_type: Optional[str] = None) -> List[Dict]:
        """Get effectiveness data for attack methods."""
        if not self.client:
            return []
        
        try:
            where_clause = "WHERE 1=1"
            params = {}
            
            if method_name:
                where_clause += " AND method_name = %(method_name)s"
                params["method_name"] = method_name
            
            if method_type:
                where_clause += " AND method_type = %(method_type)s"
                params["method_type"] = method_type
            
            result = self.client.query(f"""
                SELECT 
                    method_name,
                    method_type,
                    category,
                    success_rate,
                    avg_confidence,
                    total_uses,
                    successful_uses,
                    effectiveness_score,
                    vulnerability_types,
                    last_used
                FROM attack_methods 
                {where_clause}
                ORDER BY effectiveness_score DESC, success_rate DESC
            """, params)
            
            return [dict(row) for row in result.result_rows]
        except Exception as e:
            print(f"❌ Failed to get method effectiveness: {e}")
            return []
    
    def store_adaptive_intelligence(self, intelligence_data: Dict[str, Any]) -> bool:
        """Store learned patterns for adaptive attack selection."""
        if not self.client:
            return False
        
        try:
            self.client.command("""
                INSERT INTO adaptive_intelligence VALUES (
                    %(pattern_id)s,
                    %(website_pattern)s,
                    %(vulnerability_type)s,
                    %(effective_attacks)s,
                    %(ineffective_attacks)s,
                    %(success_probability)s,
                    %(confidence_threshold)s,
                    %(context_indicators)s,
                    %(recommendation_metadata)s,
                    now(),
                    now()
                )
            """, intelligence_data)
            return True
        except Exception as e:
            print(f"❌ Failed to store adaptive intelligence: {e}")
            return False
    
    def get_attack_statistics(self, website_url: Optional[str] = None, days_back: int = 30) -> Dict[str, Any]:
        """Get comprehensive attack statistics."""
        if not self.client:
            return {}
        
        try:
            where_clause = "WHERE timestamp >= now() - INTERVAL %(days_back)s DAY"
            params = {"days_back": days_back}
            
            if website_url:
                where_clause += " AND website_url = %(website_url)s"
                params["website_url"] = website_url
            
            # Overall statistics
            stats_result = self.client.query(f"""
                SELECT 
                    COUNT(*) as total_attacks,
                    SUM(success) as successful_attacks,
                    AVG(confidence) as avg_confidence,
                    COUNT(DISTINCT website_url) as unique_websites,
                    COUNT(DISTINCT attack_type) as unique_attack_types
                FROM attack_findings 
                {where_clause}
            """, params)
            
            # Vulnerability type breakdown
            vuln_result = self.client.query(f"""
                SELECT 
                    vulnerability_type,
                    COUNT(*) as count,
                    AVG(confidence) as avg_confidence
                FROM attack_findings 
                {where_clause} AND success = 1
                GROUP BY vulnerability_type
                ORDER BY count DESC
            """, params)
            
            # Attack type effectiveness
            attack_result = self.client.query(f"""
                SELECT 
                    attack_type,
                    COUNT(*) as total_uses,
                    SUM(success) as successful_uses,
                    AVG(confidence) as avg_confidence,
                    (SUM(success) * 100.0 / COUNT(*)) as success_rate
                FROM attack_findings 
                {where_clause}
                GROUP BY attack_type
                ORDER BY success_rate DESC
            """, params)
            
            stats = dict(stats_result.result_rows[0]) if stats_result.result_rows else {}
            stats["vulnerability_breakdown"] = [dict(row) for row in vuln_result.result_rows]
            stats["attack_effectiveness"] = [dict(row) for row in attack_result.result_rows]
            
            return stats
        except Exception as e:
            print(f"❌ Failed to get attack statistics: {e}")
            return {}
    
    def close(self):
        """Close database connection."""
        if self.client:
            self.client.close()

# Global database instance
db = ClickHouseDatabase()
