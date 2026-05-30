# ai_core/performance_optimized.py

from functools import lru_cache

# -------------------------------
# Caching for Repeated Requests
# -------------------------------
@lru_cache(maxsize=1000)
def cached_ats_score(profile_hash):
    # Simulated ATS computation
    return hash(profile_hash) % 100

# -------------------------------
# Batch Processing
# -------------------------------
def batch_resume_processing(resume_list, process_func):
    results = []
    for resume in resume_list:
        results.append(process_func(resume))
    return results

# -------------------------------
# Fast Decision Engine
# -------------------------------
def fast_decision(score):
    if score >= 75:
        return "Selected"
    elif score >= 55:
        return "Hold / Review"
    return "Rejected"
