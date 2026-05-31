# ats_engine/experience_parser.py - Experience parsing & relevance scoring for Zecpath AI.

import re
import os
import json
from datetime import datetime

# -------------------------------
# Role Similarity Mapping
# -------------------------------
ROLE_SIMILARITY = {
    "developer": ["engineer", "programmer", "software developer"],
    "engineer": ["developer", "specialist", "tool design engineer", "die design engineer", "mold design engineer"],
    "analyst": ["data analyst", "business analyst", "data-driven tooling analyst"],
    "manager": ["team lead", "project manager", "supervisor", "tool room manager", "die shop manager"],
    
    # Manufacturing / Tool & Die trade specific mapping
    "machinist": ["tool maker", "die maker", "mold maker", "operator", "cnc machinist"],
    "tool maker": ["machinist", "die maker", "mold maker", "junior tool maker", "trainee tool die maker"],
    "die maker": ["tool maker", "machinist", "mold maker", "progressive die maker", "sheet metal die maker"],
    "mold maker": ["tool maker", "machinist", "die maker", "injection mold maker", "blow mold maker"],
    "operator": ["machinist", "edm operator", "cnc machinist"]
}

# -------------------------------
# Extract Experience Entries
# -------------------------------
MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
}

MONTH_NAMES = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def extract_experience_blocks(text):
    if not text:
        return []
        
    experiences = []
    lines = text.split("\n")
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
            
        # Clean bullet prefix if any
        line_str = re.sub(r"^[-\*•▪●\s]+", "", line_str).strip()
        
        # 1. Look for Month-Year to Month-Year or Month-Year to Present (case-insensitive)
        month_pattern = (
            r"(?i)\(?(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})"
            r"\s*[-–—to\s]*\s*"
            r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|present)[a-z]*(?:\s+(\d{4}))?\)?"
        )
        
        # 2. Look for Year-Year or Year-Present (case-insensitive)
        year_pattern = (
            r"(?i)\(?(\d{4})\s*[-–—to\s]+\s*\b(\d{4}|present)\b\)?"
        )
        
        match_month = re.search(month_pattern, line_str)
        match_year = re.search(year_pattern, line_str)
        
        if match_month:
            m_start_name = match_month.group(1).lower()
            start_year = int(match_month.group(2))
            m_end_name = match_month.group(3).lower()
            end_year_str = match_month.group(4)
            
            start_month_num = MONTHS.get(m_start_name[:3], 1)
            
            if m_end_name == "present":
                end_year = datetime.now().year
                end_month_num = datetime.now().month
            else:
                end_year = int(end_year_str) if end_year_str else start_year
                end_month_num = MONTHS.get(m_end_name[:3], 1)
                
            start_month_idx = start_year * 12 + start_month_num
            end_month_idx = end_year * 12 + end_month_num
            
            duration_months = end_month_idx - start_month_idx
            if duration_months < 0:
                duration_months = 0
            duration_years = duration_months / 12.0
            
            raw_company_role = line_str[:match_month.start()].strip()
            company = re.sub(r"^[,\-\s]+|[,\-\s\(\)]+$", "", raw_company_role).strip()
            
            experiences.append({
                "company": company if company else "Unknown",
                "start_year": start_year,
                "start_month": start_month_num,
                "start_month_idx": start_month_idx,
                "end_year": end_year,
                "end_month": end_month_num,
                "end_month_idx": end_month_idx,
                "duration_months": duration_months,
                "duration_years": int(round(duration_years))
            })
            
        elif match_year:
            start_year = int(match_year.group(1))
            end_val = match_year.group(2).lower()
            
            start_month = 1
            if end_val == "present":
                end_year = datetime.now().year
                end_month = datetime.now().month
                start_month_idx = start_year * 12 + start_month
                end_month_idx = end_year * 12 + end_month
                duration_months = end_month_idx - start_month_idx
                duration_years = end_year - start_year
            else:
                end_year = int(end_val)
                end_month = 1
                start_month_idx = start_year * 12 + start_month
                end_month_idx = end_year * 12 + end_month
                duration_years = end_year - start_year
                duration_months = duration_years * 12
                
            if duration_months < 0:
                duration_months = 0
            if duration_years < 0:
                duration_years = 0
                
            raw_company_role = line_str[:match_year.start()].strip()
            company = re.sub(r"^[,\-\s]+|[,\-\s\(\)]+$", "", raw_company_role).strip()
            
            experiences.append({
                "company": company if company else "Unknown",
                "start_year": start_year,
                "start_month": start_month,
                "start_month_idx": start_month_idx,
                "end_year": end_year,
                "end_month": end_month,
                "end_month_idx": end_month_idx,
                "duration_months": duration_months,
                "duration_years": duration_years
            })
            
    return experiences

# -------------------------------
# Extract Job Titles (Simple Logic)
# -------------------------------
def extract_roles(text):
    if not text:
        return []
        
    text_lower = text.lower()
    found_roles = []
    
    # Check compound roles first
    compound_roles = [
        "tool & die maker", "tool and die maker", "tool die maker", "die design engineer", 
        "mold design engineer", "tool design engineer", "cnc tool maker",
        "cnc machinist", "edm operator", "mold maker", "die maker", "tool maker",
        "software developer", "project manager", "tool room manager", "die shop manager"
    ]
    for role in compound_roles:
        if role in text_lower:
            found_roles.append(role)
            
    # Generic roles fallback
    roles = ["developer", "engineer", "manager", "analyst", "intern", "machinist", "operator", "technician"]
    for role in roles:
        if role in text_lower:
            found_roles.append(role)
            
    return list(set(found_roles))

# -------------------------------
# Total Experience Calculation
# -------------------------------
def calculate_total_experience(experiences):
    if not experiences:
        return 0
    return sum([exp["duration_years"] for exp in experiences])

def calculate_total_experience_months(experiences):
    if not experiences:
        return 0
    return sum([exp.get("duration_months", exp["duration_years"] * 12) for exp in experiences])

# -------------------------------
# Gap Detection
# -------------------------------
def is_temporary_experience(exp):
    company_lower = exp.get("company", "").lower()
    temp_keywords = ["intern", "apprentice", "trainee", "helper", "assistant", "student", "co-op"]
    return any(k in company_lower for k in temp_keywords)

def extract_education_max_year(text):
    if not text:
        return None
    lines = text.split("\n")
    in_edu = False
    edu_text = []
    for line in lines:
        line_lower = line.strip().lower()
        if "education" in line_lower:
            in_edu = True
            continue
        if in_edu:
            if any(h in line_lower for h in ["experience", "projects", "skills", "certifications", "summary"]):
                break
            edu_text.append(line)
            
    combined_edu = "\n".join(edu_text) if edu_text else text
    years = [int(y) for y in re.findall(r"\b(20\d{2}|19\d{2})\b", combined_edu)]
    return max(years) if years else None

def detect_gaps(experiences, max_edu_year=None):
    if len(experiences) < 2:
        return []
        
    gaps = []
    has_month = all("start_month_idx" in exp for exp in experiences)
    
    if has_month:
        sorted_exp = sorted(experiences, key=lambda x: x["start_month_idx"])
        for i in range(1, len(sorted_exp)):
            prev_exp = sorted_exp[i-1]
            curr_exp = sorted_exp[i]
            prev_end_idx = prev_exp["end_month_idx"]
            curr_start_idx = curr_exp["start_month_idx"]
            
            # Skip gaps that occur during college education or around temporary roles
            prev_end_year = prev_exp["end_year"]
            if max_edu_year and prev_end_year <= max_edu_year:
                continue
            if is_temporary_experience(prev_exp) or is_temporary_experience(curr_exp):
                continue
                
            if curr_start_idx > prev_end_idx + 1:
                gap_months = curr_start_idx - prev_end_idx - 1
                gap_years = round(gap_months / 12.0)
                
                prev_month = prev_exp.get("end_month", 12)
                prev_year = prev_exp["end_year"]
                curr_month = curr_exp.get("start_month", 1)
                curr_year = curr_exp["start_year"]
                
                prev_month_str = MONTH_NAMES[prev_month] if 1 <= prev_month <= 12 else str(prev_month)
                curr_month_str = MONTH_NAMES[curr_month] if 1 <= curr_month <= 12 else str(curr_month)
                
                gaps.append({
                    "gap_years": gap_years,
                    "gap_months": gap_months,
                    "between": f"{prev_month_str} {prev_year} - {curr_month_str} {curr_year}"
                })
    else:
        sorted_exp = sorted(experiences, key=lambda x: x["start_year"])
        for i in range(1, len(sorted_exp)):
            prev_exp = sorted_exp[i-1]
            curr_exp = sorted_exp[i]
            prev_end = prev_exp["end_year"]
            curr_start = curr_exp["start_year"]
            
            # Skip gaps that occur during college education or around temporary roles
            if max_edu_year and prev_end <= max_edu_year:
                continue
            if is_temporary_experience(prev_exp) or is_temporary_experience(curr_exp):
                continue
                
            if curr_start > prev_end:
                gaps.append({
                    "gap_years": curr_start - prev_end,
                    "gap_months": (curr_start - prev_end) * 12,
                    "between": f"{prev_end} - {curr_start}"
                })
    return gaps

# -------------------------------
# Overlap Detection
# -------------------------------
def detect_overlaps(experiences):
    if len(experiences) < 2:
        return []
        
    overlaps = []
    has_month = all("start_month_idx" in exp for exp in experiences)
    
    for i in range(len(experiences)):
        for j in range(i+1, len(experiences)):
            exp1 = experiences[i]
            exp2 = experiences[j]
            
            if has_month:
                starts_within_range = (exp1["start_month_idx"] >= exp2["start_month_idx"] and exp1["start_month_idx"] < exp2["end_month_idx"])
                other_starts_within_range = (exp2["start_month_idx"] >= exp1["start_month_idx"] and exp2["start_month_idx"] < exp1["end_month_idx"])
            else:
                starts_within_range = (exp1["start_year"] >= exp2["start_year"] and exp1["start_year"] < exp2["end_year"])
                other_starts_within_range = (exp2["start_year"] >= exp1["start_year"] and exp2["start_year"] < exp1["end_year"])
                
            if starts_within_range or other_starts_within_range:
                overlaps.append((exp1, exp2))
    return overlaps

# -------------------------------
# Dynamic JD Role Matching
# -------------------------------
def load_jd_profiles():
    jd_dir = os.path.join("data", "processed_jds")
    profiles = []
    if os.path.exists(jd_dir):
        for file in os.listdir(jd_dir):
            if file.endswith(".json"):
                try:
                    with open(os.path.join(jd_dir, file), "r", encoding="utf-8") as f:
                        profiles.append(json.load(f))
                except Exception:
                    pass
    return profiles

def determine_target_role(candidate_roles, filename, jd_profiles):
    software_keywords = {"developer", "software developer", "programmer", "software engineer", "frontend developer", "fullstack developer", "analyst"}
    is_software = any(role.lower().strip() in software_keywords or "developer" in role.lower() or "software" in role.lower() for role in candidate_roles)
    
    # Also check filename as fallback
    if "developer" in filename.lower() or "software" in filename.lower():
        is_software = True
        
    has_mfg = any("tool" in r.lower() or "die" in r.lower() or "mold" in r.lower() or "machinist" in r.lower() or "operator" in r.lower() for r in candidate_roles)
    
    if is_software and not has_mfg:
        return "unknown"
        
    best_title = None
    best_score = -1
    for jd in jd_profiles:
        title = jd.get("job_title", "").lower().strip()
        if not title:
            continue
        score = 0
        for role in candidate_roles:
            role_lower = role.lower().strip()
            if role_lower == title:
                score += 10
            elif role_lower in title or title in role_lower:
                score += 5
            else:
                words1 = set(role_lower.split())
                words2 = set(title.split())
                intersect = words1.intersection(words2)
                score += len(intersect)
                
        # Break ties using job title specificity/length
        if score > best_score or (score == best_score and (best_title is None or len(title) > len(best_title))):
            best_score = score
            best_title = jd.get("job_title", "")
            
    if best_title and best_score > 0:
        return best_title
    
    if any(r in ["machinist", "tool maker", "die maker"] for r in candidate_roles):
        return "tool maker"
    return "unknown"

# -------------------------------
# Relevance Scoring
# -------------------------------
def calculate_relevance(candidate_roles, job_role):
    if not candidate_roles or not job_role:
        return 0.0
        
    job_role = job_role.lower().strip()
    
    ignored_dilution = {"intern", "apprentice", "trainee", "helper", "assistant", "specialist"}
    filtered_roles = [r for r in candidate_roles if r.lower().strip() not in ignored_dilution]
    if not filtered_roles:
        filtered_roles = candidate_roles
        
    score = 0.0
    for role in filtered_roles:
        role = role.lower().strip()
        pattern = r"\b" + re.escape(job_role) + r"\b"
        rev_pattern = r"\b" + re.escape(role) + r"\b"
        if role == job_role or re.search(pattern, role) or re.search(rev_pattern, job_role):
            score += 1.0
        elif role in ROLE_SIMILARITY.get(job_role, []):
            score += 0.7
        else:
            matched_similarity = False
            for base_key, synonyms in ROLE_SIMILARITY.items():
                job_role_matches = (base_key in job_role or job_role in base_key or any(s in job_role for s in synonyms))
                role_matches = (base_key in role or role in base_key or any(s in role for s in synonyms))
                if job_role_matches and role_matches:
                    score += 0.7
                    matched_similarity = True
                    break
            if not matched_similarity:
                if any(role in assoc for assoc in ROLE_SIMILARITY.values() if job_role in assoc):
                    score += 0.5
            
    percentage = (score / len(filtered_roles)) * 100
    return round(min(percentage, 100.0), 2)

if __name__ == "__main__":
    import os
    import json
    
    print("\n--- ZECPATH STANDALONE EXPERIENCE PARSER & RELEVANCE ENGINE TEST ---")
    processed_dir = os.path.join("data", "processed_resumes")
    
    if os.path.exists(processed_dir):
        files = [f for f in os.listdir(processed_dir) if f.endswith(".txt")]
        if files:
            # Let's test the first processed resume text
            test_file = os.path.join(processed_dir, files[0])
            print(f"Executing experience analysis on: {test_file}")
            try:
                import sys
                sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
                from parsers.section_classifier import detect_sections
                
                with open(test_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                sections = detect_sections(content)
                exp_text = "\n".join(sections.get("experience", []))
                
                experiences = extract_experience_blocks(exp_text)
                roles = extract_roles(content)
                total_exp = calculate_total_experience(experiences)
                gaps = detect_gaps(experiences)
                overlaps = detect_overlaps(experiences)
                
                # Run relevance scoring against a sample job role
                # If the candidate's resume has 'developer', we score against 'developer'
                # If they have 'machinist' or 'tool maker', we score against 'tool maker'
                target_role = "developer"
                if any(r in ["machinist", "tool maker", "die maker"] for r in roles):
                    target_role = "tool maker"
                    
                relevance = calculate_relevance(roles, target_role)
                
                # Format to JSON
                output = {
                    "candidate_file": os.path.basename(test_file),
                    "extracted_experiences": experiences,
                    "extracted_roles": roles,
                    "total_experience_years": total_exp,
                    "detected_gaps": gaps,
                    "detected_overlaps": [
                        [o[0]["company"], o[1]["company"]] for o in overlaps
                    ],
                    "target_job_role": target_role,
                    "role_relevance_score": relevance
                }
                
                print("\n[Structured Experience Object (JSON)]:")
                print("--------------------------------------------------")
                print(json.dumps(output, indent=2))
                print("--------------------------------------------------")
                print("--- Standalone Experience parsing completed successfully ---\n")
            except Exception as ex:
                print(f"Error parsing: {ex}")
        else:
            print("No processed resumes found in data/processed_resumes/. Run 'python run_parser.py' first.")
    else:
        print("Data directory 'data/processed_resumes' not found. Run 'python run_parser.py' first.")
