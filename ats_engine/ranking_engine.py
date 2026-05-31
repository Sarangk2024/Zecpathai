# ats_engine/ranking_engine.py - Candidate ranking & shortlisting engine for Zecpath AI.

# -------------------------------
# Threshold Configuration
# -------------------------------
THRESHOLDS = {
    "shortlist": 75,
    "review": 50
}

# -------------------------------
# Sort Candidates by Score
# -------------------------------
def rank_candidates(candidates):
    """
    Sort candidates in descending order of final_score and assign a sequential rank.
    """
    ranked = sorted(
        candidates,
        key=lambda x: x.get("final_score", 0.0),
        reverse=True
    )
    # Assign rank
    for idx, candidate in enumerate(ranked, start=1):
        candidate["rank"] = idx
    return ranked

# -------------------------------
# Candidate Classification
# -------------------------------
def classify_candidate(score):
    if score >= THRESHOLDS["shortlist"]:
        return "Shortlisted"
    elif score >= THRESHOLDS["review"]:
        return "Review"
    else:
        return "Rejected"

# -------------------------------
# Apply Shortlisting Logic
# -------------------------------
def apply_shortlisting(candidates):
    for candidate in candidates:
        score = candidate.get("final_score", 0.0)
        candidate["status"] = classify_candidate(score)
    return candidates

# -------------------------------
# Top Candidate Selector
# -------------------------------
def get_top_candidates(candidates, top_n=5):
    return candidates[:top_n]

# -------------------------------
# Complete Pipeline Function
# -------------------------------
def ranking_pipeline(candidates):
    ranked = rank_candidates(candidates)
    shortlisted = apply_shortlisting(ranked)
    top_candidates = get_top_candidates(shortlisted)
    return {
        "ranked_list": shortlisted,
        "top_candidates": top_candidates
    }

# -------------------------------
# Recruiter-Friendly Output Format
# -------------------------------
def format_recruiter_summary(job_id, candidates):
    total = len(candidates)
    shortlisted = sum(1 for c in candidates if c.get("status") == "Shortlisted")
    review = sum(1 for c in candidates if c.get("status") == "Review")
    rejected = sum(1 for c in candidates if c.get("status") == "Rejected")
    
    top_candidates = []
    for c in candidates[:5]:
        top_candidates.append({
            "candidate_id": c.get("candidate_id"),
            "score": c.get("final_score"),
            "status": c.get("status")
        })
        
    return {
        "job_id": job_id,
        "summary": {
            "total_candidates": total,
            "shortlisted": shortlisted,
            "review": review,
            "rejected": rejected
        },
        "top_candidates": top_candidates
    }
