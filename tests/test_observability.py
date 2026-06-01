# tests/test_observability.py

from observability.logging import log_event
from observability.metrics import calculate_metrics, check_alerts
from observability.audit import audit_log

def test_metrics():
    # Specifications-requested test structure
    log = log_event("ATS", "test", {})
    assert "service" in log
    assert log["service"] == "ATS"
    assert log["event_type"] == "test"

def test_calculate_metrics():
    res = calculate_metrics(9, 10, [1.2, 1.8, 2.5, 0.9])
    assert res["success_rate"] == 0.9
    assert res["avg_latency"] == 1.6

    res_empty = calculate_metrics(0, 0, [])
    assert res_empty["success_rate"] == 0
    assert res_empty["avg_latency"] == 0

def test_check_alerts():
    # Alert conditions checks
    alerts_none = check_alerts({"avg_latency": 1.5, "success_rate": 0.95})
    assert len(alerts_none) == 0

    alerts_latency = check_alerts({"avg_latency": 2.5, "success_rate": 0.95})
    assert "High latency detected" in alerts_latency
    assert len(alerts_latency) == 1

    alerts_all = check_alerts({"avg_latency": 2.5, "success_rate": 0.85})
    assert "High latency detected" in alerts_all
    assert "Low success rate" in alerts_all
    assert len(alerts_all) == 2

def test_audit_log():
    audit = audit_log("decision_modified", "recruiter_sarang", "C101")
    assert audit["action"] == "decision_modified"
    assert audit["user"] == "recruiter_sarang"
    assert audit["candidate_id"] == "C101"
    assert "timestamp" in audit
