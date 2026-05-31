import re
import os
import json
import sys
from datetime import datetime

sys.path.append(".")

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
}

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

def extract_experience_blocks(text):
    if not text:
        return []
    experiences = []
    lines = text.split("\n")
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        line_str = re.sub(r"^[-\*•▪●\s]+", "", line_str).strip()
        month_pattern = (
            r"(?i)\(?(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})"
            r"\s*[-–—to\s]*\s*"
            r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|present)[a-z]*(?:\s+(\d{4}))?\)?"
        )
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

def extract_roles(text):
    if not text:
        return []
    text_lower = text.lower()
    found_roles = []
    compound_roles = [
        "tool & die maker", "tool and die maker", "tool die maker", "die design engineer", 
        "mold design engineer", "tool design engineer", "cnc tool maker",
        "cnc machinist", "edm operator", "mold maker", "die maker", "tool maker",
        "software developer", "project manager", "tool room manager", "die shop manager"
    ]
    for role in compound_roles:
        if role in text_lower:
            found_roles.append(role)
    roles = ["developer", "engineer", "manager", "analyst", "intern", "machinist", "operator", "technician"]
    for role in roles:
        if role in text_lower:
            found_roles.append(role)
    return list(set(found_roles))

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
    
    # Also check if filename indicates developer/software
    if "developer" in filename.lower() or "software" in filename.lower():
        is_software = True
        
    if is_software and not any("tool" in role.lower() or "die" in role.lower() or "mold" in role.lower() or "machinist" in role.lower() for role in candidate_roles):
        return "developer"
        
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
        if score > best_score or (score == best_score and (best_title is None or len(title) > len(best_title))):
            best_score = score
            best_title = jd.get("job_title", "")
            
    if best_title and best_score > 0:
        return best_title
    
    if any(r in ["machinist", "tool maker", "die maker"] for r in candidate_roles):
        return "tool maker"
    return "developer"

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

def extract_education_max_year(text):
    if not text:
        return None
    # Let's isolate the Education section if possible, or search the whole text
    # A simple search for B.Tech/Diploma/B.E/Education followed by years or Completed year
    # Let's find all years in the education lines
    lines = text.split("\n")
    in_edu = False
    edu_text = []
    for line in lines:
        line_lower = line.lower()
        if "education" in line_lower:
            in_edu = True
            continue
        if in_edu:
            # Check if entering next major section
            if any(h in line_lower for h in ["experience", "projects", "skills", "certifications", "summary"]):
                break
            edu_text.append(line)
    
    combined_edu = "\n".join(edu_text) if edu_text else text
    years = [int(y) for y in re.findall(r"\b(20\d{2}|19\d{2})\b", combined_edu)]
    return max(years) if years else None

def is_temporary_experience(exp):
    company_lower = exp.get("company", "").lower()
    temp_keywords = ["intern", "apprentice", "trainee", "helper", "assistant", "student", "co-op"]
    return any(k in company_lower for k in temp_keywords)

def detect_gaps_improved(experiences, max_edu_year=None):
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
            
            # Skip gap if it's before/during graduation or involves temporary positions
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
                
                MONTH_NAMES = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
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

jd_profiles = load_jd_profiles()
processed_dir = "data/processed_resumes"
files = [f for f in os.listdir(processed_dir) if f.endswith(".txt")]

print(f"{'Filename':<52} | {'Matched JD Role':<35} | {'Gaps?':<5} | {'Relevance':<8}")
print("-" * 110)
for f in files:
    content = open(os.path.join(processed_dir, f), encoding="utf-8").read()
    from parsers.section_classifier import detect_sections
    sections = detect_sections(content)
    exp_text = "\n".join(sections.get("experience", []))
    exps = extract_experience_blocks(exp_text)
    roles = extract_roles(content)
    
    target_role = determine_target_role(roles, f, jd_profiles)
    relevance = calculate_relevance(roles, target_role)
    
    max_edu_year = extract_education_max_year(content)
    gaps = detect_gaps_improved(exps, max_edu_year)
    
    gaps_str = "YES" if gaps else "NO"
    print(f"{f:<52} | {target_role:<35} | {gaps_str:<5} | {relevance:<8.1f}%")
