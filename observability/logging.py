# observability/logging.py

import datetime

def log_event(service, event_type, data):
    return {
        "service": service,
        "event_type": event_type,
        "data": data,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
