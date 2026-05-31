# screening_ai/eligibility_engine.py - Automated eligibility cutoff check logic.

# -------------------------------
# Default Eligibility Rules
# -------------------------------
DEFAULT_RULES = {
    "min_ats_score": 70,
    "mandatory_skills": [],
    "min_experience": 0,
    "max_experience": 10,
    "allowed_locations": [],
    "availability_required": False
}

# -------------------------------
# Edge Case Helper
# -------------------------------
def safe_value(value, default):
    return value if value is not None else default

# -------------------------------
# Skill Matching Check
# -------------------------------
def check_mandatory_skills(candidate_skills, required_skills):
    candidate_skills = safe_value(candidate_skills, [])
    required_skills = safe_value(required_skills, [])
    
    if not required_skills:
        return True
        
    candidate_skills = [s.lower().strip() for s in candidate_skills]
    required_skills = [s.lower().strip() for s in required_skills]
    return all(skill in candidate_skills for skill in required_skills)

# -------------------------------
# Experience Check
# -------------------------------
def check_experience(candidate_exp, min_exp, max_exp):
    candidate_exp = safe_value(candidate_exp, 0)
    min_exp = safe_value(min_exp, 0)
    max_exp = safe_value(max_exp, 100)
    return min_exp <= candidate_exp <= max_exp

# -------------------------------
# Location Check
# -------------------------------
def check_location(candidate_location, allowed_locations):
    candidate_location = safe_value(candidate_location, "")
    allowed_locations = safe_value(allowed_locations, [])
    
    if not allowed_locations:
        return True
    return candidate_location.lower().strip() in [loc.lower().strip() for loc in allowed_locations]

# -------------------------------
# Availability Check
# -------------------------------
def check_availability(is_available, required):
    is_available = safe_value(is_available, True)
    required = safe_value(required, False)
    
    if not required:
        return True
    return is_available

# -------------------------------
# Main Eligibility Function
# -------------------------------
def evaluate_candidate(candidate, rules=None):
    if rules is None:
        rules = DEFAULT_RULES
        
    # Get values with safe default fallbacks
    ats_score = safe_value(candidate.get("final_score"), 0)
    skills = safe_value(candidate.get("skills"), [])
    experience = safe_value(candidate.get("total_experience"), 0)
    location = safe_value(candidate.get("location"), "")
    available = safe_value(candidate.get("available"), True)
    
    # Rule checks
    skill_ok = check_mandatory_skills(skills, rules.get("mandatory_skills"))
    exp_ok = check_experience(experience, rules.get("min_experience"), rules.get("max_experience"))
    loc_ok = check_location(location, rules.get("allowed_locations"))
    avail_ok = check_availability(available, rules.get("availability_required"))
    
    min_ats = rules.get("min_ats_score", 70)
    
    # Decision logic
    if ats_score >= min_ats and skill_ok and exp_ok and loc_ok and avail_ok:
        status = "Eligible"
    elif ats_score >= (min_ats - 15) and skill_ok and exp_ok and loc_ok and avail_ok:
        status = "Review"
    else:
        status = "Rejected"
        
    return {
        "candidate_id": candidate.get("candidate_id"),
        "eligibility_status": status,
        "checks": {
            "ats_score": ats_score,
            "skill_match": skill_ok,
            "experience_match": exp_ok,
            "location_match": loc_ok,
            "availability_match": avail_ok
        }
    }

# -------------------------------
# Batch Evaluation Pipeline
# -------------------------------
def evaluate_candidates_batch(candidates, rules=None):
    if rules is None:
        rules = DEFAULT_RULES
    results = []
    for candidate in candidates:
        result = evaluate_candidate(candidate, rules)
        results.append(result)
    return results
