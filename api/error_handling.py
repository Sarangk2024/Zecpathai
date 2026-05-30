# api/error_handling.py

import time

def retry_request(func, retries=3):
    for attempt in range(retries):
        try:
            return func()
        except Exception:
            if attempt < retries - 1:
                time.sleep(0.1)
    return {"error": "Max retries exceeded"}
