# demo/full_pipeline_simulation.py

def run_demo_pipeline(candidate_id):
    # Simulated scores matching candidate quality levels
    scores = {
        "C001": {"final": 85.0, "decision": "Selected"},
        "C002": {"final": 68.0, "decision": "Hold / Review"},
        "C003": {"final": 45.0, "decision": "Rejected"}
    }
    return {
        "candidate_id": candidate_id,
        "result": scores.get(candidate_id, {"final": 0.0, "decision": "Rejected"})
    }

if __name__ == "__main__":
    for c in ["C001", "C002", "C003"]:
        print(run_demo_pipeline(c))
