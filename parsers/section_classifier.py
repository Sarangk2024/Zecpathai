# parsers/section_classifier.py - Resume section classifier for Zecpath AI.

import re

# -------------------------------
# Section Keywords Dictionary
# -------------------------------
SECTION_KEYWORDS = {
    "skills": ["skills", "technical skills", "skill set", "key skills", "expertise", "technical competencies", "core competencies", "competencies", "technical qualifications"],
    "experience": ["experience", "work experience", "professional experience", "employment history", "work history", "experience credentials", "work experience credentials"],
    "education": ["education", "academic background", "qualification", "academic profile", "academic details", "education credentials", "educational qualifications", "academic qualifications"],
    "certifications": ["certifications", "certificates", "licenses", "courses", "professional certifications"],
    "projects": ["projects", "project work", "academic projects", "key projects", "core academic projects", "projects worked on"],
    "summary": ["summary", "profile", "objective", "professional summary", "about me", "career summary"]
}

# -------------------------------
# Normalize Text
# -------------------------------
def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------------
# Paragraph & Bullet Point Rebuilder
# -------------------------------
def rebuild_blocks(lines):
    rebuilt = []
    current_block = []
    # Match standard months, years, "present" to detect dates in headers
    date_pat = r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|present|\d{4})\b"
    
    # Common conjunctions, prepositions, determiners, or adjectives that cannot end a sentence
    continuation_words = {
        "a", "an", "the", "and", "or", "but", "of", "for", "with", "at", 
        "by", "from", "to", "in", "on", "as", "normalized", "our", "their", 
        "its", "your", "my", "his", "her", "this", "that", "these", 
        "those", "which", "who", "whom", "whose", "using", "through", "across",
        "under", "over", "between", "among", "throughout", "during"
    }
    
    for i, line in enumerate(lines):
        line_str = line.strip()
        if not line_str:
            continue
            
        is_bullet = line_str.startswith(("-", "*", "•", "▪", "●", " -"))
        is_header = bool(re.search(date_pat, line_str, re.IGNORECASE))
        
        # Lookahead: if the next line starts with a bullet, the current line is a header
        is_followed_by_bullet = False
        if i + 1 < len(lines):
            next_line_str = lines[i+1].strip()
            if next_line_str.startswith(("-", "*", "•", "▪", "●", " -")):
                # Only treat as a heading if it starts with uppercase or digit
                if line_str and (line_str[0].isupper() or line_str[0].isdigit()):
                    is_followed_by_bullet = True
                    if current_block:
                        last_line = current_block[-1].strip()
                        # Extract the last word, stripped of punctuation
                        words = re.findall(r"\b\w+\b", last_line)
                        if words:
                            last_word = words[-1].lower()
                            if last_word in continuation_words:
                                is_followed_by_bullet = False
                
        should_start_new = is_bullet or is_header or is_followed_by_bullet
        
        if not current_block:
            current_block.append(line_str)
        elif should_start_new:
            rebuilt.append(" ".join(current_block))
            current_block = [line_str]
        else:
            # Check for hyphenated word split across line breaks
            if current_block[-1].endswith("-"):
                current_block[-1] = current_block[-1][:-1] + line_str
            else:
                current_block.append(line_str)
                
    if current_block:
        rebuilt.append(" ".join(current_block))
    return rebuilt

# -------------------------------
# Education Cleaning Helper
# -------------------------------
def clean_education_line(line):
    if not line:
        return ""
    # 1. Clean CGPA/GPA and everything after it (handle cases like KeralaCGPA without word boundaries)
    line = re.sub(r"(?i)c?gpa.*", "", line)
    
    # 2. Clean percentage/score at the end of the line
    line = re.sub(r"(?i)\b\d+\s*(?:%|percent|percentage|score|marks)?\s*$", "", line)
    
    # 3. Clean "Gold Medalist"
    line = re.sub(r"(?i)\bGold Medalist\b", "", line)
    
    # 4. Clean Course duration info (e.g. "4-Year Course", "3-Year Course")
    line = re.sub(r"(?i)\b\d+[- ](?:Year|Yr)\s+(?:Course|Program)?\b", "", line)
    
    # 5. Clean Year ranges (e.g. 2022 - 2026, 2022 2026, etc.)
    line = re.sub(r"\b(19|20)\d{2}\s*[-–—\s]+\s*(19|20)\d{2}\b", "", line)
    
    # 6. Clean standalone years (e.g. 2022, 2021)
    line = re.sub(r"\b(19|20)\d{2}\b", "", line)
    
    # 7. Clean action verbs/status words related to completion
    line = re.sub(r"(?i)\b(?:completed|graduated|graduation|passing|passed|pursuing|ongoing|passout|enrolled)\s*(?:in)?\b", "", line)
    
    # 8. Clean up extra punctuation/spaces
    line = line.strip()
    line = re.sub(r"^[,\-\s]+|[,\-\s]+$", "", line)
    line = re.sub(r"\s+", " ", line)
    line = line.strip()
    
    return line

# -------------------------------
# Section Detection Logic
# -------------------------------
def detect_sections(text):
    if not text:
        return {}
        
    lines = text.split("\n")
    sections = {}
    current_section = "other"
    
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
            
        clean_line = normalize_text(stripped_line)
        
        # Heading Check: A heading line should be relatively short to avoid matching full sentences
        is_heading = False
        found_section = None
        
        if len(clean_line) < 35:
            for section, keywords in SECTION_KEYWORDS.items():
                for keyword in keywords:
                    # Match exact heading, or heading at the start, or surrounded by delimiters
                    # E.g. "=== SKILLS ===" or "SKILLS:" or "SKILLS"
                    clean_keyword = keyword.lower()
                    # Pattern matching
                    pattern = r"^(?:[^a-z0-9]*)\b" + re.escape(clean_keyword) + r"\b(?:[^a-z0-9]*)$"
                    if re.match(pattern, clean_line):
                        found_section = section
                        is_heading = True
                        break
                    
                    # Alternatively, check starts with
                    if clean_line.startswith(clean_keyword) and len(clean_line) <= len(clean_keyword) + 2:
                        found_section = section
                        is_heading = True
                        break
                if found_section:
                    break
                    
        # Update current section and content lists
        if is_heading and found_section:
            current_section = found_section
            if current_section not in sections:
                sections[current_section] = []
        else:
            sections.setdefault(current_section, []).append(stripped_line)
            
    # Clean up empty list mappings and rebuild blocks for narrative sections
    cleaned_sections = {}
    for sec, lines_list in sections.items():
        if lines_list:
            if sec in ["summary", "experience", "projects"]:
                cleaned_sections[sec] = rebuild_blocks(lines_list)
            elif sec == "education":
                cleaned_education = []
                for line in lines_list:
                    cleaned = clean_education_line(line)
                    if cleaned:
                        cleaned_education.append(cleaned)
                cleaned_sections[sec] = cleaned_education
            else:
                cleaned_sections[sec] = lines_list
            
    return cleaned_sections

if __name__ == "__main__":
    import os
    import json
    
    print("\n--- ZECPATH STANDALONE RESUME SECTION SEGMENTATION TEST ---")
    processed_dir = os.path.join("data", "processed_resumes")
    
    if os.path.exists(processed_dir):
        files = [f for f in os.listdir(processed_dir) if f.endswith(".txt")]
        if files:
            # Let's test the first processed resume text
            test_file = os.path.join(processed_dir, files[0])
            print(f"Executing section segmentation on: {test_file}")
            try:
                with open(test_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                result = detect_sections(content)
                # Output a pretty formatted JSON structure of sections
                print("\n[Segmented Sections (JSON)]:")
                print("--------------------------------------------------")
                # Format to show first 2 lines of each section so we don't dump too much text
                preview_result = {}
                for sec, lines in result.items():
                    preview_result[sec] = lines[:3] + ["..."] if len(lines) > 3 else lines
                print(json.dumps(preview_result, indent=2))
                print("--------------------------------------------------")
                print("--- Standalone Section classification completed successfully ---\n")
            except Exception as ex:
                print(f"Error classifying: {ex}")
        else:
            print("No processed resumes found in data/processed_resumes/. Run 'python run_parser.py' first.")
    else:
        print("Data directory 'data/processed_resumes' not found. Run 'python run_parser.py' first.")
