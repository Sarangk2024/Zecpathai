# ats_engine/skill_extractor.py - Skill extraction engine for Zecpath AI.

import re

# -------------------------------
# Master Skill Dictionary
# -------------------------------
# -------------------------------
# Master Skill Dictionary
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
    
    # Tool & Die / Machining / Manufacturing
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
# Skill Stacks Mapping
# -------------------------------
SKILL_STACKS = {
    "mern": ["mongodb", "express", "react", "node"],
    "mean": ["mongodb", "express", "angular", "node"],
    "cad_cam_stack": ["autocad", "solidworks", "catia", "nx"]
}

# -------------------------------
# Normalize Text
# -------------------------------
def clean_text(text):
    if not text:
        return ""
    # Standardize dashes
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2012", "-").replace("\u2212", "-")
    # Replace colons and slashes with spaces to keep words separated
    text = text.replace(":", " ").replace("/", " ")
    text = text.lower()
    # Retain alphanumeric, spaces, periods, commas, hyphens, pluses, and hashes (for C++, C#)
    text = re.sub(r"[^a-z0-9\s\.\,\-\+\#]", "", text)
    return text

# -------------------------------
# Extract Skills
# -------------------------------
def extract_skills(text):
    cleaned_text = clean_text(text)
    extracted = []
    
    # Check individual skills
    for skill, variants in SKILL_DB.items():
        for variant in variants:
            cleaned_variant = clean_text(variant)
            pattern = r"\b" + re.escape(cleaned_variant) + r"\b"
            if re.search(pattern, cleaned_text):
                extracted.append(skill)
                break
                    
    # Check skill stacks
    for stack, skills in SKILL_STACKS.items():
        cleaned_stack = clean_text(stack)
        pattern = r"\b" + re.escape(cleaned_stack) + r"\b"
        if re.search(pattern, cleaned_text):
            extracted.extend(skills)
            
    return list(set(extracted))

# -------------------------------
# Skill Confidence Scoring Logic
# -------------------------------
def calculate_confidence(skill, text):
    cleaned_text = clean_text(text)
    variants = list(SKILL_DB.get(skill, [skill]))
    
    # Include stack keywords that represent this skill
    for stack, skills in SKILL_STACKS.items():
        if skill in skills:
            variants.append(stack)
            
    occurrences = 0
    for variant in variants:
        cleaned_variant = clean_text(variant)
        pattern = r"\b" + re.escape(cleaned_variant) + r"\b"
        occurrences += len(re.findall(pattern, cleaned_text))
        
    if occurrences >= 3:
        return 0.95
    elif occurrences == 2:
        return 0.85
    elif occurrences == 1:
        return 0.75
    else:
        return 0.0

def extract_skills_with_confidence(text):
    skills = extract_skills(text)
    results = []
    for skill in skills:
        confidence = calculate_confidence(skill, text)
        if confidence > 0.0:
            results.append({
                "skill": skill,
                "confidence": round(confidence, 2)
            })
    # Sort by confidence descending
    return sorted(results, key=lambda x: x["confidence"], reverse=True)

if __name__ == "__main__":
    import os
    import json
    
    print("\n--- ZECPATH STANDALONE SKILL EXTRACTION ENGINE TEST ---")
    processed_dir = os.path.join("data", "processed_resumes")
    
    if os.path.exists(processed_dir):
        files = [f for f in os.listdir(processed_dir) if f.endswith(".txt")]
        if files:
            # Let's test the first processed resume text
            test_file = os.path.join(processed_dir, files[0])
            print(f"Executing skill extraction on: {test_file}")
            try:
                with open(test_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                result = extract_skills_with_confidence(content)
                print("\n[Extracted Skills with Confidence (JSON)]:")
                print("--------------------------------------------------")
                print(json.dumps(result, indent=2))
                print("--------------------------------------------------")
                print("--- Standalone Skill extraction completed successfully ---\n")
            except Exception as ex:
                print(f"Error extracting: {ex}")
        else:
            print("No processed resumes found in data/processed_resumes/. Run 'python run_parser.py' first.")
    else:
        print("Data directory 'data/processed_resumes' not found. Run 'python run_parser.py' first.")
