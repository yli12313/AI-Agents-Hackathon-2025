#!/usr/bin/env python3
"""
Initialize ClickHouse Cloud database with schema.
Run this once to create tables: python init_clickhouse.py
"""
import os
import clickhouse_connect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def init_clickhouse():
    """Initialize ClickHouse with schema"""
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
        
        # Test connection
        result = client.command("SELECT 1")
        print(f"✅ Connection test passed: {result}")
        
        # Create findings table
        print("\n📋 Creating findings table...")
        client.command("""
            CREATE TABLE IF NOT EXISTS findings (
                timestamp DateTime DEFAULT now(),
                category String,
                severity String,
                success UInt8,
                confidence Float32 DEFAULT 0.0,
                snippet String DEFAULT ''
            ) ENGINE = MergeTree()
            ORDER BY timestamp
        """)
        print("✅ findings table created")
        
        # Create plans table
        print("📋 Creating plans table...")
        client.command("""
            CREATE TABLE IF NOT EXISTS plans (
                timestamp DateTime DEFAULT now(),
                category String,
                eta_hours Float32,
                cost_hours Float32,
                roi_per_hour Float32,
                risk_level String DEFAULT ''
            ) ENGINE = MergeTree()
            ORDER BY timestamp
        """)
        print("✅ plans table created")
        
        # Verify tables exist
        print("\n🔍 Verifying tables...")
        tables = client.query("SHOW TABLES").result_set
        table_names = [t[0] for t in tables]
        print(f"✅ Tables found: {table_names}")
        
        if 'findings' in table_names and 'plans' in table_names:
            print("\n🎉 ClickHouse initialization complete!")
            print("\nYou can now run your Streamlit app:")
            print("  streamlit run streamlit.py")
        else:
            print("\n⚠️ Warning: Expected tables not found")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure your .env file has:")
        print("  CH_HOST=your-clickhouse-cloud-host")
        print("  CH_USER=default")
        print("  CH_PASSWORD=your-password")
        print("  CH_SECURE=true")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(init_clickhouse())
