# security/audit_log.py

import datetime

def log_event(event_type, candidate_id, data):
    return {
        "event_type": event_type,
        "candidate_id": candidate_id,
        "data": data,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
