"""
Mock ClickHouse implementation for demo purposes.
Stores data in-memory when ClickHouse is unavailable.
"""
import datetime as dt
from typing import List, Dict, Any

class MockClickHouseClient:
    """In-memory storage that mimics ClickHouse API"""
    
    def __init__(self):
        self.findings = []
        self.plans = []
        
    def command(self, sql: str) -> None:
        """Execute a SQL command (INSERT)"""
        sql_lower = sql.lower()
        
        if 'insert into findings' in sql_lower:
            # Parse the INSERT statement (simplified)
            self.findings.append({
                'timestamp': dt.datetime.now(),
                'raw_sql': sql
            })
        elif 'insert into plans' in sql_lower:
            self.plans.append({
                'timestamp': dt.datetime.now(),
                'raw_sql': sql
            })
    
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute a SELECT query"""
        # Simple mock responses for common queries
        if 'from plans' in sql.lower():
            return [
                {
                    'category': 'PII_EXPOSURE',
                    'avg_roi': 1.8,
                    'avg_eta': 6.0,
                    'occurrences': len(self.plans) or 1
                },
                {
                    'category': 'OTHER',
                    'avg_roi': 0.1,
                    'avg_eta': 1.0,
                    'occurrences': max(0, len(self.plans) - 1)
                }
            ]
        elif 'from findings' in sql.lower():
            return [{
                'timestamp': dt.datetime.now(),
                'category': 'PII_EXPOSURE',
                'severity': 'HIGH',
                'success': 1
            }] if self.findings else []
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about stored data"""
        return {
            'total_findings': len(self.findings),
            'total_plans': len(self.plans),
            'high_severity_count': len([f for f in self.findings if 'HIGH' in str(f)]),
        }

# Global instance
_mock_client = MockClickHouseClient()

def get_mock_client():
    """Get the singleton mock client instance"""
    return _mock_client
