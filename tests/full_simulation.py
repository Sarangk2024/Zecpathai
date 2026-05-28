# tests/full_simulation.py

import random

def simulate_candidate():
    return {
        "ats": random.randint(60, 90),
        "screening": random.randint(60, 85),
        "hr": random.randint(65, 90),
        "technical": random.randint(60, 95),
        "machine_test": random.randint(60, 95)
    }

def run_full_simulation(n=50):
    results = []
    for _ in range(n):
        scores = simulate_candidate()
        # Compute dynamic weights final score
        avg_score = sum(scores.values()) / len(scores)
        decision = "Selected" if avg_score >= 75 else "Rejected"
        results.append({
            "scores": scores,
            "decision": decision
        })
    return results
