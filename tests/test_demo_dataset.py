# tests/test_demo_dataset.py

import json
import os
from demo.full_pipeline_simulation import run_demo_pipeline

def test_demo():
    # Specifications-requested test structure
    result = run_demo_pipeline("C001")
    assert result["result"]["decision"] == "Selected"

def test_pipeline_outcomes():
    res_avg = run_demo_pipeline("C002")
    assert res_avg["result"]["decision"] == "Hold / Review"
    assert res_avg["result"]["final"] == 68.0

    res_weak = run_demo_pipeline("C003")
    assert res_weak["result"]["decision"] == "Rejected"
    assert res_weak["result"]["final"] == 45.0

def test_json_load():
    json_path = r"c:\Users\kutta\OneDrive\Desktop\zecpath\demo\demo_dataset.json"
    assert os.path.exists(json_path)
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert "job_description" in data
    assert "candidates" in data
    assert len(data["candidates"]) == 3
    assert data["candidates"][0]["name"] == "Arjun Nair"
