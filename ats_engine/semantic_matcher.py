# ats_engine/semantic_matcher.py - Semantic Resume to JD Matching for Zecpath AI.

import numpy as np

# -------------------------------
# Load Model & Handle Fallbacks
# -------------------------------
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    # Initialize the lightweight semantic embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    USE_TRANSFORMERS = True
except Exception:
    USE_TRANSFORMERS = False
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# Generate Embeddings
# -------------------------------
def get_embedding(text):
    if USE_TRANSFORMERS:
        try:
            return model.encode(text, convert_to_numpy=True)
        except Exception:
            return None
    return None

# -------------------------------
# Compute Similarity
# -------------------------------
def compute_similarity(text1, text2):
    if not text1 or not text2:
        return 0.0
        
    text1_str = str(text1).strip()
    text2_str = str(text2).strip()
    
    if not text1_str or not text2_str:
        return 0.0
        
    if USE_TRANSFORMERS:
        try:
            emb1 = get_embedding(text1_str)
            emb2 = get_embedding(text2_str)
            if emb1 is not None and emb2 is not None:
                similarity = cosine_similarity([emb1], [emb2])[0][0]
                return round(float(similarity), 4)
        except Exception:
            # Fall back to TF-IDF if model execution fails
            pass
            
    # TF-IDF Cosine Similarity Fallback with Term Standardization and Power Scaling
    try:
        import re
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        def standardize_vocab(t):
            t = t.lower()
            replacements = {
                r"\bmould(?:ing|s|ed)?\b": "mold",
                r"\bmachin(?:ist|ing|es|ed)?\b": "machine",
                r"\bprogramm(?:er|ing|ed)?\b": "program",
                r"\bdesign(?:er|ing|ed)?\b": "design",
                r"\bdie\s*mak(?:er|ing)?\b": "diemaker",
                r"\btool\s*mak(?:er|ing)?\b": "toolmaker",
                r"\boperat(?:or|ing|ed)?\b": "operate",
                r"\bfabricat(?:or|ing|ed)?\b": "fabricate",
                r"\bweld(?:er|ing)?\b": "weld",
                r"\bfitt(?:er|ing)?\b": "fit",
                r"\bsolidworks?\b": "solidworks",
                r"\bautocads?\b": "autocad",
                r"\bgd&?t\b": "gdt",
                r"\bdeveloper\b": "develop",
                r"\bprogramming\b": "program"
            }
            for pattern, rep in replacements.items():
                t = re.sub(pattern, rep, t)
            return t

        t1_std = standardize_vocab(text1_str)
        t2_std = standardize_vocab(text2_str)
        
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([t1_std, t2_std])
        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        
        # Scale the TF-IDF similarity to map to semantic space ranges
        if similarity > 0.0:
            similarity = similarity ** 0.4
            
        return round(float(similarity), 4)
    except Exception:
        return 0.0

# -------------------------------
# Section-wise Matching
# -------------------------------
def match_resume_to_jd(resume, jd):
    results = {}
    
    # 1. Skills Matching
    resume_skills_list = resume.get("skills", []) or resume.get("extracted_skills", [])
    resume_skills = " ".join(resume_skills_list)
    jd_skills = " ".join(jd.get("required_skills", []))
    results["skills_similarity"] = compute_similarity(resume_skills, jd_skills)
    
    # 2. Experience Matching
    experiences = resume.get("experience", []) or resume.get("extracted_experiences", [])
    exp_roles = []
    for exp in experiences:
        role = exp.get("role", "") or exp.get("company", "")
        if role:
            exp_roles.append(role)
    resume_exp = " ".join(exp_roles)
    jd_role = jd.get("job_title", "")
    results["experience_similarity"] = compute_similarity(resume_exp, jd_role)
    
    # 3. Project Matching
    projects = resume.get("projects", [])
    proj_descs = []
    for proj in projects:
        desc = proj.get("description", "") or proj.get("name", "")
        if desc:
            proj_descs.append(desc)
    resume_proj = " ".join(proj_descs)
    
    # JD description check with fallbacks
    jd_desc = jd.get("job_description_text", "") or jd.get("cleaned_text", "") or jd.get("raw_text", "")
    results["project_similarity"] = compute_similarity(resume_proj, jd_desc)
    
    # Final Score (Weighted with Dynamic Redistribution for Missing Sections)
    w_skills = 0.4
    w_exp = 0.3
    w_proj = 0.3
    
    if not proj_descs and not exp_roles:
        w_skills = 1.0
        w_exp = 0.0
        w_proj = 0.0
    elif not proj_descs:
        w_skills = 0.55
        w_exp = 0.45
        w_proj = 0.0
    elif not exp_roles:
        w_skills = 0.55
        w_exp = 0.0
        w_proj = 0.45
        
    final_score = (
        w_skills * results["skills_similarity"] +
        w_exp * results["experience_similarity"] +
        w_proj * results["project_similarity"]
    )
    results["final_similarity_score"] = round(final_score * 100, 2)
    return results

# -------------------------------
# Threshold Classification
# -------------------------------
def classify_match(score):
    if score >= 70:
        return "Strong Match"
    elif score >= 50:
        return "Moderate Match"
    else:
        return "Weak Match"
