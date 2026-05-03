# tests/test_jd_parser.py - Unit tests for Job Description parser.

import pytest
from parsers.jd_parser import clean_text, extract_skills, extract_experience, extract_role, extract_education, parse_job_description

def test_clean_text():
    raw_input = "We are looking for a Tool & Die Maker! @ Pune (2-5 years experience)."
    expected = "we are looking for a tool die maker pune 2-5 years experience."
    assert clean_text(raw_input) == expected

def test_extract_skills():
    text = "Requires SolidWorks, AutoCAD, CNC programming, and Python developer skills."
    skills = extract_skills(text)
    assert "solidworks" in skills
    assert "autocad" in skills
    assert "cnc" in skills
    assert "python" in skills
    assert "django" not in skills

def test_extract_experience_range():
    text1 = "Must have 2–5 years of work experience in mold design."
    text2 = "Experience range: 3 to 6 yrs."
    assert extract_experience(text1) == 2
    assert extract_experience(text2) == 3

def test_extract_experience_single():
    text = "Candidate with 3+ years experience preferred."
    assert extract_experience(text) == 3

def test_extract_experience_fresher():
    text = "Apprentice role. Freshers can apply. Stipend-based."
    assert extract_experience(text) == 0

def test_extract_role():
    text = "We are hiring a CNC Machinist with expertise in VMC operations."
    assert extract_role(text) == "cnc machinist"
    
    text2 = "Required senior operations manager for tool room."
    assert extract_role(text2) == "operations manager tool room" or "manager" in extract_role(text2)

def test_extract_education():
    text1 = "Minimum qualification: ITI in Fitter / Tool Maker trade."
    text2 = "Must possess Diploma in Mechanical or B.Tech degree."
    text3 = "Requires Diploma in Civil Engineering or Computer Science."
    assert extract_education(text1) == "ITI in Fitter / Tool Making"
    assert extract_education(text2) == "Diploma in Mechanical / B.Tech/B.E"
    assert extract_education(text3) == "Not Specified"

def test_parse_job_description():
    jd_text = """
    Looking for a Tool Design Engineer with 3+ years experience.
    Must have SolidWorks, AutoCAD, and GD&T knowledge.
    B.E / B.Tech required.
    """
    res = parse_job_description(jd_text)
    assert res["job_title"] == "tool design engineer"
    assert "solidworks" in res["required_skills"]
    assert "autocad" in res["required_skills"]
    assert "gd_t" in res["required_skills"]
    assert res["min_experience_years"] == 3
    assert res["education_required"] == "B.Tech/B.E"
