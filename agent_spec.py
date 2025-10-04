name: redbot-prescriber
objective: >
  Attack our consented chatbot once, structure any vuln (PII, prompt-injection),
  and produce a prescriptive remediation plan with owners, ETA (hours), acceptance tests, rollback,
  plus a 1-line exec summary. Do NOT run unit/integration tests. Keep total runtime under 30s.

tools:
  - attack_target             # HTTP POST to TARGET_URL with a crafted payload
  - structure_finding         # local parser → VulnerabilityReport JSON
  - build_plan                # deterministic PlanSpec (ETA, cost, steps, tests, rollback)
  - persist_clickhouse        # INSERT finding/plan rows for Top-ROI chart
  - notify_comment            # either GitHub Issue or Discord webhook

memory:
  enabled: true
  keys: [last_attack_type, last_success, last_eta_hours]

run_policy:
  max_steps: 5
  timeout_seconds: 30
  stop_when:
    - plan_built_and_persisted
    - comment_posted
