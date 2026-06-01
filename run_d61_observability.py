# run_d61_observability.py

import json
from observability.logging import log_event
from observability.metrics import calculate_metrics, check_alerts
from observability.audit import audit_log

def main():
    print("\n==========================================================================================")
    print("ZECPATH AI OBSERVABILITY & MONITORING SYSTEM RUNNER (DAY 61)")
    print("==========================================================================================\n")

    # 1. Logging Event Schema
    print("--- [STEP 1] EXECUTING LOG EVENT GENERATION ---")
    log = log_event(
        service="ATS",
        event_type="score_generated",
        data={
            "candidate_id": "C101",
            "score": 78
        }
    )
    print("Sample Log Output:")
    print(json.dumps(log, indent=2))

    # 2. Metric Calculations & Alerts
    print("\n--- [STEP 2] RUNNING METRICS CALCULATION & ALERTS CHECK ---")
    
    # Healthy System
    metrics_healthy = calculate_metrics(success=95, total=100, response_times=[1.2, 1.4, 0.8, 1.1])
    alerts_healthy = check_alerts(metrics_healthy)
    print(f"Metrics (Healthy): {metrics_healthy} -> Active Alerts: {alerts_healthy}")

    # Degradation System
    metrics_degraded = calculate_metrics(success=85, total=100, response_times=[2.5, 3.1, 1.8, 2.8])
    alerts_degraded = check_alerts(metrics_degraded)
    print(f"Metrics (Degraded): {metrics_degraded} -> Active Alerts: {alerts_degraded}")

    # 3. Monitoring Dashboard Design
    print("\n--- [STEP 3] MONITORING DASHBOARD OVERVIEW LAYOUT ---")
    dashboard = """
    ---------------------------------------------------------------------
    |                        AI System Overview                         |
    ---------------------------------------------------------------------
    | Total Candidates Processed: 1,245  | Active Interviews: 18        |
    | Success Rate: 98.4%                | Avg Response Time: 0.92s     |
    ---------------------------------------------------------------------
    |                         Module Performance                        |
    ---------------------------------------------------------------------
    | ATS Accuracy: 90%                  | Screening Accuracy: 85%      |
    | HR Accuracy: 87%                   | Technical Accuracy: 89%      |
    ---------------------------------------------------------------------
    |                          Alerts & Issues                          |
    ---------------------------------------------------------------------
    | [WARN] High latency detected on technical API endpoint.           |
    ---------------------------------------------------------------------
    """
    print(dashboard)

    # 4. Audit Log Record
    print("--- [STEP 4] RUNNING DECISION AUDIT LOGGER ---")
    audit = audit_log(action="score_modified", user="recruiter_sarang", candidate_id="C101")
    print("Sample Audit Record:")
    print(json.dumps(audit, indent=2))

    print("\n------------------------------------------------------------------------------------------")
    print("Day 61 Observability & Monitoring Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
