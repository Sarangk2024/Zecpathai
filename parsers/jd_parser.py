# parsers/jd_parser.py - Job Description parser for Zecpath AI system.

import re

# -------------------------------
# Skill Dictionary (Extended for both Tech and Tool & Die / Manufacturing)
# -------------------------------
# -------------------------------
# Skill Dictionary (Extended for both Tech and Tool & Die / Manufacturing)
# -------------------------------
SKILL_DB = {
    # Tech/Software
    "python": ["python", "py"],
    "django": ["django"],
    "javascript": ["javascript", "js"],
    "react": ["react", "reactjs"],
    "node": ["node", "nodejs"],
    "sql": ["sql", "mysql", "postgresql", "query optimization", "normalized schema", "normalized database"],
    "mongodb": ["mongodb", "mongo"],
    "express": ["express", "expressjs"],
    "java": ["java"],
    "c_lang": ["c"],
    "c_sharp": ["c#", "csharp", "c sharp"],
    "fastapi": ["fastapi"],
    "docker": ["docker", "containerization", "containerized"],
    "git": ["git", "github", "gitlab", "version control"],
    "tensorflow": ["tensorflow", "tf"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "asp_net": ["asp.net", "asp net", "asp.net mvc"],
    "jwt": ["jwt", "json web token", "json web tokens"],
    "agile": ["agile", "scrum"],
    "oop": ["oop", "object-oriented", "object oriented"],
    "dsa": ["dsa", "data structures", "algorithms", "data structures and algorithms"],
    "dbms": ["dbms", "database management", "database management system", "database management systems"],
    "machine_learning": ["machine learning", "ml", "ai/ml", "image classification", "model training", "model training evaluation", "transfer learning", "deep learning", "nlp", "efficientnet", "mobilenetv2"],
    
    # Manufacturing / Tool & Die / Engineering Skills
    "cnc": ["cnc", "vmc", "cnc programming", "g-code", "m-code", "cnc machine", "cnc machines", "vmc machine", "vmc machines"],
    "cad_cam": ["cad/cam", "cad cam", "cad", "cam", "computer aided design"],
    "solidworks": ["solidworks", "cswp"],
    "catia": ["catia", "catia v5"],
    "nx": ["nx", "unigraphics", "nx cad", "siemens nx"],
    "autocad": ["autocad"],
    "gd_t": ["gd&t", "gdt", "geometric dimensioning", "geometric dimensioning & tolerancing", "geometric dimensioning and tolerancing"],
    "milling": ["milling", "mill", "mills", "milling machine", "milling machines", "conventional milling"],
    "lathe": ["lathe", "lathes", "lathe machine", "lathe machines", "conventional lathes", "conventional lathe", "turning", "cylindrical turning"],
    "grinding": ["grinding", "grinder", "grinders", "surface grinding", "surface grinder", "surface grinders", "conventional grinding"],
    "edm": ["edm", "wire cut edm", "sinker edm", "spark edm", "spark erosion"],
    "mold_design": ["mold design", "mold designer", "mold designers", "mould design", "mould designer", "mould designers"],
    "die_design": ["die design", "die designer", "die designers"],
    "injection_molding": ["injection molding", "injection mould", "injection moulding", "plastic mold", "plastic mould", "plastic molds", "plastic moulds", "injection molds"],
    "stamping": ["stamping", "sheet metal stamping", "press tools", "press tool", "stamping dies", "stamping die", "progressive stamping"],
    "cmm": ["cmm", "coordinate measuring machine", "coordinate measuring machines"],
    "additive_manufacturing": ["3d printing", "additive manufacturing", "3d print", "3d printing"],
    "heat_treatment": ["heat treatment", "hardening", "tempering", "quenched", "annealing"],
    "fitting": ["fitting", "fitter", "fitters", "die fitting", "bench work", "filing", "scraping", "hand tools"],
    "jigs_fixtures": ["jigs and fixtures", "jigs & fixtures", "fixtures", "fixture", "jig", "jigs", "mould fixtures", "mould fixture"],
    "metrology": ["metrology", "vernier", "verniers", "caliper", "calipers", "vernier caliper", "vernier calipers", "micrometer", "micrometers", "height master", "height gauge", "height gauges", "bevel protractor", "bevel protractors", "bore gauge", "bore gauges", "slip gauge", "slip gauges", "optical comparator", "optical comparators", "profile projector", "profile projectors", "toolmaker microscope", "toolmaker microscopes", "dial test indicator", "dial test indicators"],
    "preventive_maintenance": ["preventive maintenance", "maintenance", "maintenance and repair", "maintenance cycles", "repair", "repairs", "maintenance schedules"],
    "die_assembly": ["die assembly", "mold assembly", "mould assembly", "assembly", "assemblies", "assembling", "assembled"],
    "tool_steels": ["tool steels", "tool steel", "d2", "h13", "o1", "vanadis", "tungsten carbide", "tungsten carbides", "carbide", "carbides"],
    "blueprint_reading": ["blueprint reading", "blueprints", "engineering blueprints", "engineering drawings", "drawing reading", "interpret drawings", "blueprint", "engineering graphics"],
    "drilling": ["drilling", "drill", "drills", "drill machine", "drill machines", "radial drill", "drilling machine", "drill press", "drill presses"],
    "hot_runner": ["hot runner", "hot-runner", "hot runner systems", "hot runner blocks", "manifold assemblies", "manifold assembly"],
    "moldflow": ["moldflow", "mold flow", "moldflow analysis", "moldflow simulation", "moldflow simulations"],
    "tolerance_analysis": ["tolerance stack-up", "tolerance analysis", "tolerance stackup", "stack-up analysis", "tolerance stack-up analysis"],
    "blow_molding": ["blow mold", "blow molds", "blow moulding", "blow molding"],
    "strip_layout": ["strip layout", "strip layouts"],
    "clearance": ["clearance", "clearance allowances", "slide clearance", "shear clearances", "assembly clearances"],
    "tooling_components": ["guide pillars", "bushings", "guide pillar", "bushing", "guide pillars and bushings", "pillars", "ejector pins", "ejector pin", "wear plates", "leader pins", "punches", "dies", "punch", "die", "spring cylinders", "spring cylinder", "springs", "springs", "ejector plate", "cavity split", "cavity splits", "slider", "sliders", "angle pin", "lifter", "lifters", "lifter design", "lifter designs"],
    "polishing": ["polishing", "polish", "mirror finish", "mirror-finished", "mold polishing", "mould polishing", "polishing mold cavities"],
    "cooling_design": ["cooling channels", "cooling channel", "water cooling paths", "cooling system", "cooling layout", "cooling calculations"],
    "venting": ["venting", "vent heights", "air vents"],
    "hydraulic_systems": ["hydraulic core pull", "core pull", "hydraulic systems", "hydraulic core pull systems"],
    "shaping": ["shaper", "shapers", "shaping machine", "shaping machines"],
    "welding": ["welding", "welder", "arc welding", "tig welding", "mig welding"],
    "gating_design": ["gating", "gate positions", "gate design", "gating design", "sprue", "runner gating"],
    "shrinkage": ["shrinkage", "shrinkage coefficients", "material shrinkage", "shrinkage parameters"],
    
    # Soft/Non-Technical Skills
    "communication": ["communication", "communication skills", "verbal skills"],
    "leadership": ["leadership", "team leadership", "management"]
}

# -------------------------------
# Normalize Text
# -------------------------------
def clean_text(text):
    if not text:
        return ""
    # Standardize dashes before stripping special characters (using unicode escapes to prevent encoding mismatch)
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2012", "-").replace("\u2212", "-")
    text = text.lower()
    # Remove unwanted characters except alpha, numeric, spaces, dots, commas, hyphens, and slashes
    text = re.sub(r"[^a-z0-9\s\.\,\-\/]", "", text)
    # Standardize multiple spaces to a single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------------
# Extract Skills
# -------------------------------
def extract_skills(text):
    text = text.lower()
    found_skills = []
    for skill, variants in SKILL_DB.items():
        for variant in variants:
            # Use word boundaries or check if variant is in text
            # For short words like 'js', 'py' we check word boundaries to prevent false positives in words like 'pyramid'
            if len(variant) <= 2:
                pattern = r"\b" + re.escape(variant) + r"\b"
                if re.search(pattern, text):
                    found_skills.append(skill)
                    break
            else:
                if variant in text:
                    found_skills.append(skill)
                    break
    return sorted(list(set(found_skills)))

# -------------------------------
# Extract Experience
# -------------------------------
def extract_experience(text):
    text = text.lower()
    
    # Check for "freshers" or "fresher" -> 0 years
    if "fresher" in text or "entry-level" in text or "apprentice" in text:
        # Wait, check if experience is actually specified nearby
        pass
        
    # Check range pattern first: e.g. "3-6 years", "1–2 years", "2 to 5 yrs"
    range_match = re.search(r"(\d+)\s*(?:-|–|to)\s*(\d+)\s*(?:years|yrs|year|yr)", text)
    if range_match:
        return int(range_match.group(1))
        
    # Check single pattern: e.g. "3+ years", "3 years", "5 yrs"
    single_match = re.search(r"(\d+)\+?\s*(?:years|yrs|year|yr)", text)
    if single_match:
        return int(single_match.group(1))
        
    if "fresher" in text or "apprenticeship" in text or "stipend-based" in text:
        return 0
        
    return None

# -------------------------------
# Extract Role
# -------------------------------
def extract_role(text):
    text = text.lower()
    
    # Check specific compound roles first to avoid generic matches
    compound_roles = [
        "tool & die maker", "tool and die maker", "tool die maker", "die design engineer", 
        "mold design engineer", "tool design engineer", "cnc tool maker",
        "cnc machinist", "edm operator", "mold maker", "die maker", "tool maker"
    ]
    for role in compound_roles:
        if role in text:
            return role
            
    # Generic roles fallback
    roles = [
        "developer", "engineer", "manager", "analyst", "specialist", 
        "technician", "supervisor", "inspector", "helper", "assistant",
        "trainee", "apprentice"
    ]
    for role in roles:
        if role in text:
            return role
            
    return "unknown"

# -------------------------------
# Extract Education
# -------------------------------
DISCIPLINE_MAP = {
    "tool & die": "Tool & Die Making",
    "tool and die": "Tool & Die Making",
    "tool die": "Tool & Die Making",
    "tool making": "Tool Making",
    "toolmaker": "Tool Making",
    "tool maker": "Tool Making",
    "mechanical": "Mechanical",
    "mech anical": "Mechanical",
    "machinist": "Machinist",
    "ma chinist": "Machinist",
    "mold": "Mold Technology",
    "mould": "Mold Technology",
    "plastic": "Plastics",
    "plastic s": "Plastics",
    "cnc": "CNC",
    "vmc": "VMC",
    "production": "Production",
    "prod uction": "Production",
    "automobile": "Automotive",
    "automotive": "Automotive",
    "manufacturing": "Manufacturing",
    "mechatronics": "Mechatronics",
    "turner": "Turner",
    "fitter": "Fitter",
    "technical certification": "Technical Certification"
}

def extract_disciplines(text, keyword):
    # Search with word boundaries first to avoid matching inside larger words (like 'iti' in 'responsibilities')
    pattern = r"\b" + re.escape(keyword) + r"\b"
    match = re.search(pattern, text)
    if match:
        idx = match.start()
    else:
        idx = text.find(keyword)
        if idx == -1:
            return ""
            
    window = text[idx:idx+80]
    found = []
    temp = window.lower()
    matches_info = []
    
    for key in sorted(DISCIPLINE_MAP.keys(), key=len, reverse=True):
        start = 0
        while True:
            pos = temp.find(key, start)
            if pos == -1:
                break
            # Verify if this position is already covered by a longer match
            already_covered = False
            for covered_pos, covered_len in matches_info:
                if pos >= covered_pos and pos < covered_pos + covered_len:
                    already_covered = True
                    break
            if not already_covered:
                matches_info.append((pos, len(key)))
                found.append((pos, DISCIPLINE_MAP[key]))
            start = pos + 1
            
    # Sort by the position (pos) in the window
    found.sort(key=lambda x: x[0])
    
    ordered_found = []
    for pos, name in found:
        if name not in ordered_found:
            ordered_found.append(name)
            
    if ordered_found:
        return " in " + " / ".join(ordered_found)
    return ""

def extract_education(text):
    text = text.lower()
    matches = []
    
    # Check ITI variations (using word boundaries to avoid matching in "activities" or "critical")
    has_iti = bool(re.search(r"\biti\b", text))
        
    # Check Diploma variations (only if in a related field)
    has_diploma = False
    if "diploma" in text:
        related_keywords = [
            "tool", "die", "mechanical", "machinist", "mold", "mould", 
            "plastic", "cnc", "vmc", "production", "automobile", 
            "automotive", "manufacturing", "mechatronics", "turner", 
            "fitter", "technical certification"
        ]
        is_related = False
        start = 0
        while True:
            idx = text.find("diploma", start)
            if idx == -1:
                break
            # Inspect 80 characters after "diploma"
            window = text[idx:idx+80]
            if any(kw in window for kw in related_keywords):
                is_related = True
                break
            start = idx + 1
        has_diploma = is_related
            
    # Check degree variations
    has_btech = bool("btech" in text or "b.tech" in text or "b.e" in text or "b.e." in text)
    has_mtech = bool("mtech" in text or "m.tech" in text or "m.e" in text or "m.e." in text)
    has_mba = bool("mba" in text)
    
    # Extract disciplines
    iti_disp = extract_disciplines(text, "iti") if has_iti else ""
    diploma_disp = extract_disciplines(text, "diploma") if has_diploma else ""
    
    # Find search keyword for B.Tech / B.E
    btech_kw = "b.tech" if "b.tech" in text else ("b.e" if "b.e" in text else ("btech" if "btech" in text else "b.e."))
    btech_disp = extract_disciplines(text, btech_kw) if has_btech else ""
    
    mtech_kw = "m.tech" if "m.tech" in text else ("m.e" if "m.e" in text else ("mtech" if "mtech" in text else "m.e."))
    mtech_disp = extract_disciplines(text, mtech_kw) if has_mtech else ""
    
    mba_disp = extract_disciplines(text, "mba") if has_mba else ""
    
    # Formatting and grouping
    if has_iti and has_diploma and iti_disp == diploma_disp:
        matches.append(f"ITI / Diploma{iti_disp}")
    else:
        if has_iti:
            matches.append(f"ITI{iti_disp}")
        if has_diploma:
            matches.append(f"Diploma{diploma_disp}")
            
    if has_btech:
        matches.append(f"B.Tech/B.E{btech_disp}")
    if has_mtech:
        matches.append(f"M.Tech{mtech_disp}")
    if has_mba:
        matches.append(f"MBA{mba_disp}")
        
    if matches:
        return " / ".join(matches)
        
    return "Not Specified"


# -------------------------------
# Main Parser Function
# -------------------------------
def parse_job_description(jd_text):
    cleaned = clean_text(jd_text)
    return {
        "job_title": extract_role(cleaned),
        "required_skills": extract_skills(cleaned),
        "min_experience_years": extract_experience(cleaned),
        "education_required": extract_education(cleaned),
        "raw_text": jd_text,
        "cleaned_text": cleaned
    }

if __name__ == "__main__":
    import os
    import json
    
    print("\n--- ZECPATH STANDALONE JOB DESCRIPTION PARSER TEST ---")
    jd_dir = os.path.join("data", "jd")
    
    if os.path.exists(jd_dir):
        files = [f for f in os.listdir(jd_dir) if f.endswith(".txt")]
        if files:
            # Let's test the first extracted JD file
            test_file = os.path.join(jd_dir, files[0])
            print(f"Executing extraction test on: {test_file}")
            try:
                with open(test_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                result = parse_job_description(content)
                print("\n[Structured JD Output (JSON)]:")
                print("--------------------------------------------------")
                print(json.dumps(result, indent=2))
                print("--------------------------------------------------")
                print("--- Standalone JD parsing check completed successfully ---\n")
            except Exception as ex:
                print(f"Error parsing: {ex}")
        else:
            print("No job descriptions found in data/jd/. Run 'python -m utils.split_jds' first.")
    else:
        print("Data directory 'data/jd' not found. Run 'python -m utils.split_jds' first.")
