#!/usr/bin/env python3
"""
Seed ClickHouse with dummy data for testing.
Run this to populate the database: python seed_data.py
"""
import os
import clickhouse_connect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def seed_data():
    """Insert sample data into ClickHouse"""
    print("🔗 Connecting to ClickHouse...")
    
    # Build connection parameters
    ch_host = os.getenv("CH_HOST", "localhost")
    ch_params = {
        "host": ch_host,
        "user": os.getenv("CH_USER", "default"),
        "connect_timeout": 10
    }
    
    # Add password if provided
    ch_password = os.getenv("CH_PASSWORD", "")
    if ch_password:
        ch_params["password"] = ch_password
    
    # Add secure flag for cloud connections
    if os.getenv("CH_SECURE", "false").lower() == "true":
        ch_params["secure"] = True
    else:
        ch_params["port"] = int(os.getenv("CH_PORT", "8123"))
    
    try:
        client = clickhouse_connect.get_client(**ch_params)
        print(f"✅ Connected to ClickHouse: {ch_host}")
        
        # Sample findings data
        print("\n📊 Inserting sample findings...")
        findings_data = [
            ("PII_EXPOSURE", "HIGH", 1, 0.86, "Found email: admin@company.com in response"),
            ("PII_EXPOSURE", "HIGH", 1, 0.92, "Leaked internal contact: support@corp.com"),
            ("PROMPT_INJECTION", "MEDIUM", 1, 0.75, "System prompt partially exposed"),
            ("OTHER", "LOW", 0, 0.42, "No vulnerabilities detected"),
            ("PII_EXPOSURE", "HIGH", 1, 0.88, "User data exposure detected"),
        ]
        
        for category, severity, success, confidence, snippet in findings_data:
            client.command(
                f"INSERT INTO findings VALUES (now(), '{category}', '{severity}', "
                f"{success}, {confidence}, '{snippet}')"
            )
        print(f"✅ Inserted {len(findings_data)} findings")
        
        # Sample plans data
        print("📊 Inserting sample plans...")
        plans_data = [
            ("PII_EXPOSURE", 6.0, 6.0, 1.8, "HIGH"),
            ("PII_EXPOSURE", 5.5, 5.5, 1.9, "HIGH"),
            ("PROMPT_INJECTION", 4.0, 4.0, 1.2, "MEDIUM"),
            ("OTHER", 1.0, 1.0, 0.1, "LOW"),
            ("PII_EXPOSURE", 6.5, 6.5, 1.7, "HIGH"),
        ]
        
        for category, eta, cost, roi, risk in plans_data:
            client.command(
                f"INSERT INTO plans VALUES (now(), '{category}', "
                f"{eta}, {cost}, {roi}, '{risk}')"
            )
        print(f"✅ Inserted {len(plans_data)} plans")
        
        # Verify data
        print("\n🔍 Verifying data...")
        findings_count = client.command("SELECT COUNT(*) FROM findings")
        plans_count = client.command("SELECT COUNT(*) FROM plans")
        
        print(f"✅ Total findings: {findings_count}")
        print(f"✅ Total plans: {plans_count}")
        
        # Show sample ROI data
        print("\n📊 Top ROI Opportunities:")
        roi_query = """
            SELECT 
                category,
                AVG(roi_per_hour) as avg_roi,
                AVG(eta_hours) as avg_eta,
                COUNT(*) as occurrences
            FROM plans
            GROUP BY category
            ORDER BY avg_roi DESC
        """
        roi_data = client.query(roi_query).result_set
        
        for row in roi_data:
            category, avg_roi, avg_eta, count = row
            print(f"  • {category}: ROI={avg_roi:.2f}/hr, ETA={avg_eta:.1f}h, Count={count}")
        
        print("\n🎉 Seed data inserted successfully!")
        print("\nNow run your Streamlit app and check the analytics dashboard:")
        print("  streamlit run streamlit.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(seed_data())
