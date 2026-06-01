# observability/metrics.py

def calculate_metrics(success, total, response_times):
    success_rate = success / total if total else 0
    avg_latency = sum(response_times) / len(response_times) if response_times else 0
    return {
        "success_rate": round(success_rate, 2),
        "avg_latency": round(avg_latency, 2)
    }

def check_alerts(metrics):
    alerts = []
    if metrics.get("avg_latency", 0) > 2:
        alerts.append("High latency detected")
    if metrics.get("success_rate", 0) < 0.9:
        alerts.append("Low success rate")
    return alerts
