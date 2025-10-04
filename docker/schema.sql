-- RedBot ClickHouse Schema
-- Tables for storing security findings and remediation plans

-- Findings table: stores vulnerability detection results
CREATE TABLE IF NOT EXISTS findings (
    timestamp DateTime DEFAULT now(),
    category String,
    severity String,
    success UInt8,
    confidence Float32 DEFAULT 0.0,
    snippet String DEFAULT ''
) ENGINE = MergeTree()
ORDER BY timestamp;

-- Plans table: stores remediation plans with cost/ROI metrics
CREATE TABLE IF NOT EXISTS plans (
    timestamp DateTime DEFAULT now(),
    category String,
    eta_hours Float32,
    cost_hours Float32,
    roi_per_hour Float32,
    risk_level String DEFAULT ''
) ENGINE = MergeTree()
ORDER BY timestamp;

-- View: Top ROI opportunities (for dashboard)
CREATE VIEW IF NOT EXISTS top_roi_opportunities AS
SELECT 
    category,
    MAX(timestamp) as last_seen,
    AVG(roi_per_hour) as avg_roi,
    AVG(eta_hours) as avg_eta,
    COUNT(*) as occurrences
FROM plans
GROUP BY category
ORDER BY avg_roi DESC
LIMIT 10;
