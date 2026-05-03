# parsers/education_parser.py - Education & Certification Parsing module for Zecpath AI.

import re

# -------------------------------
# Degree Mapping
# -------------------------------
DEGREE_MAP = {
    "btech": "B.Tech",
    "b.tech": "B.Tech",
    "be": "B.Tech",
    "b.e": "B.Tech",
    "mtech": "M.Tech",
    "m.tech": "M.Tech",
    "me": "M.Tech",
    "m.e": "M.Tech",
    "mba": "MBA",
    "bsc": "B.Sc",
    "b.sc": "B.Sc",
    "msc": "M.Sc",
    "m.sc": "M.Sc",
    
    # Manufacturing-specific degrees
    "diploma": "Diploma",
    "iti": "ITI"
}

# -------------------------------
# Certification Categories
# -------------------------------
CERT_CATEGORIES = {
    # Tech Certifications
    "aws": "Cloud",
    "azure": "Cloud",
    "gcp": "Cloud",
    "python": "Programming",
    "data science": "Data",
    "machine learning": "AI",
    "scrum": "Management",
    
    # Manufacturing/CAD/CAM/Quality Certifications
    "solidworks": "CAD_CAM",
    "autocad": "CAD_CAM",
    "mastercam": "CAD_CAM",
    "creo": "CAD_CAM",
    "catia": "CAD_CAM",
    "cnc": "Machining",
    "gdt": "Quality",
    "gd&t": "Quality",
    "six sigma": "Quality",
    "iso": "Quality",
    "die fitting": "Tooling",
    "die design": "Tooling",
    "mold making": "Tooling"
}

# -------------------------------
# Normalize Text
# -------------------------------
def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\.\,\-]", "", text)
    return text

# -------------------------------
# Extract Education
# -------------------------------
def extract_education(text):
    if not text:
        return []
        
    cleaned = clean_text(text)
    education_list = []
    
    # Split by lines to parse entries individually
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        line_clean = clean_text(line)
        if not line_clean:
            continue
            
        matched_degree_val = None
        
        # Look for match in degree map using regex word boundary
        for key, value in DEGREE_MAP.items():
            pattern = r"\b" + re.escape(key) + r"\b"
            if re.search(pattern, line_clean):
                matched_degree_val = value
                break
                
        if matched_degree_val:
            # Look at this line and up to 2 subsequent lines to extract year/institution
            search_lines = [line]
            for offset in range(1, 3):
                next_idx = idx + offset
                if next_idx < len(lines):
                    next_line_clean = clean_text(lines[next_idx])
                    # If it's a section header, stop searching
                    if any(next_line_clean == h or next_line_clean.startswith(h + " ") or next_line_clean.startswith(h + ":") for h in ["experience", "skills", "projects", "certifications", "summary", "languages", "interests", "expertise"]):
                        break
                    search_lines.append(lines[next_idx])
            
            combined_line = " ".join(search_lines)
            combined_line_clean = clean_text(combined_line)
            
            # Extract year
            # We want the graduation year. If there are multiple years (like "2022 2026"), take the latest year (max)
            year_match = re.findall(r"\b(20\d{2}|19\d{2})\b", combined_line)
            year = None
            if year_match:
                try:
                    year = str(max(int(y) for y in year_match))
                except ValueError:
                    year = year_match[0]
            
            # Extract field of study
            field = "Not Specified"
            # Pattern matching B.Tech in Computer Science / Diploma in Mechanical
            field_match = re.search(
                r"\b(?:in|specialization in|branch of|discipline of)\s+([a-z0-9\s&]+?)(?:\s+(?:from|completed|graduated|passed|at|university|college|institute|school|board|academy|cgpa|score|gpa)|\b\d{4}\b|\(|,|$)", 
                combined_line_clean
            )
            if field_match:
                field = field_match.group(1).strip().title()
            else:
                # Fallback keywords
                fields = ["computer science", "mechanical", "tool & die", "tooling", "electrical", "production", "information technology", "civil"]
                for f in fields:
                    if f in combined_line_clean:
                        field = f.title()
                        break
                        
            # Extract institution
            institution = "Not Extracted"
            for s_line in search_lines:
                inst_match = re.search(r"\bfrom\s+([A-Za-z0-9\s,\.-]+?)(?:\s+completed|\s+in|\s+\(|,|$)", s_line)
                if inst_match:
                    institution = inst_match.group(1).strip()
                    break
                else:
                    keywords = ["university", "college", "institute", "school", "board", "academy"]
                    found_kw = False
                    for kw in keywords:
                        if kw in s_line.lower():
                            match = re.search(r"\b([A-Za-z0-9\s,\.-]*?\b" + re.escape(kw) + r"\b[A-Za-z0-9\s,\.-]*)\b", s_line, re.IGNORECASE)
                            if match:
                                institution = match.group(1).strip()
                                # Clean up ending verbs/details/years
                                institution = re.split(r"\b(?:completed|graduated|passed|\d{4}|cgpa|score|gpa)\b", institution, flags=re.IGNORECASE)[0].strip()
                                institution = re.sub(r"[\s,\.-]+$", "", institution).strip()
                                found_kw = True
                                break
                    if found_kw:
                        break
                            
            education_list.append({
                "degree": matched_degree_val,
                "field": field,
                "institution": institution,
                "year_of_completion": year
            })
            
    # Deduplicate keeping the one with completion year if possible
    unique_edu = {}
    for edu in education_list:
        deg = edu["degree"]
        if deg not in unique_edu or (edu["year_of_completion"] and not unique_edu[deg]["year_of_completion"]):
            unique_edu[deg] = edu
            
    return list(unique_edu.values())

# -------------------------------
# Extract Certifications
# -------------------------------
def extract_certifications(text):
    if not text:
        return []
        
    text_clean = clean_text(text)
    certifications = []
    
    for keyword, category in CERT_CATEGORIES.items():
        if keyword in text_clean:
            # Extract the raw certification title from the line if possible
            lines = text.split("\n")
            cert_name = keyword.title()
            for line in lines:
                if keyword in line.lower():
                    cleaned_line = line.strip()
                    cleaned_line = re.sub(r"^[-\*•▪●\s]+", "", cleaned_line).strip()
                    if 5 <= len(cleaned_line) <= 60:
                        cert_name = cleaned_line
                    break
            certifications.append({
                "name": cert_name,
                "category": category
            })
            
    # Deduplicate by name
    seen = set()
    deduped = []
    for c in certifications:
        if c["name"].lower() not in seen:
            seen.add(c["name"].lower())
            deduped.append(c)
            
    return deduped

# -------------------------------
# Advanced AI-Ready Profile Generator
# -------------------------------
def generate_academic_profile(candidate_id, text, job_skills=None):
    edu = extract_education(text)
    certs = extract_certifications(text)
    
    education_profile = []
    for e in edu:
        try:
            year_val = int(e["year_of_completion"]) if e["year_of_completion"] else None
        except ValueError:
            year_val = None
            
        education_profile.append({
            "degree": e["degree"],
            "field": e["field"],
            "institution": e["institution"],
            "year": year_val,
            "confidence": 0.9 if e["year_of_completion"] and e["institution"] != "Not Extracted" else 0.7
        })
        
    certifications_profile = []
    for c in certs:
        relevance = 0.5
        if job_skills:
            job_skills_lower = [s.lower() for s in job_skills]
            if c["category"].lower() in job_skills_lower or c["name"].lower() in job_skills_lower:
                relevance = 0.95
        certifications_profile.append({
            "name": c["name"],
            "category": c["category"],
            "relevance_score": relevance
        })
        
    return {
        "candidate_id": candidate_id,
        "academic_profile": {
            "education": education_profile,
            "certifications": certifications_profile
        }
    }

# -------------------------------
# Education Relevance Logic
# -------------------------------
def calculate_education_relevance(candidate_degree, required_degree):
    if not candidate_degree or not required_degree:
        return 0.0
    candidate_degree = candidate_degree.lower().strip()
    required_degree = required_degree.lower().strip()
    
    if candidate_degree == required_degree:
        return 1.0
    # Postgraduate matches undergraduate requirement
    elif candidate_degree in ["m.tech", "mba", "m.e"] and required_degree in ["b.tech", "b.e"]:
        return 0.8
    # Overqualification for Diploma/ITI
    elif candidate_degree in ["b.tech", "b.e"] and required_degree in ["diploma", "iti"]:
        return 0.9
    elif candidate_degree == "diploma" and required_degree == "iti":
        return 0.8
    else:
        return 0.5

# -------------------------------
# Certification Relevance Logic
# -------------------------------
def calculate_certification_relevance(certifications, job_skills):
    score = 0
    if not certifications:
        return 0.0
    for cert in certifications:
        if cert["category"].lower() in [skill.lower() for skill in job_skills] or \
           any(skill.lower() in cert["name"].lower() for skill in job_skills):
            score += 1
    return round((score / len(certifications)) * 100, 2)
