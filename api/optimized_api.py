# api/optimized_api.py

import time

def optimized_response(data):
    start = time.time()
    # Simulate processing
    result = {"data": data}
    latency = time.time() - start
    return {
        "result": result,
        "latency_ms": round(latency * 1000, 4)
    }
