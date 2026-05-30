# tests/load_test.py

import random

def simulate_load(n=1000):
    results = []
    for _ in range(n):
        response_time = random.uniform(0.5, 1.5)
        results.append(response_time)
    avg = sum(results) / len(results)
    return {
        "avg_response": round(avg, 2),
        "max_response": round(max(results), 2)
    }

if __name__ == "__main__":
    print(simulate_load())
