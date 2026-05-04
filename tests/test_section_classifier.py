# tests/test_section_classifier.py - Unit tests for resume section classification.

import pytest
from parsers.section_classifier import detect_sections, normalize_text

def test_normalize_text():
    assert normalize_text("  WORK   EXPERIENCE  ") == "work experience"
    assert normalize_text("") == ""

def test_section_detection_basic():
    sample_text = """
    John Doe
    SKILLS
    Python, Django, SQL
    WORK EXPERIENCE
    ABC Tech - Software Developer
    Worked on APIs
    EDUCATION
    B.Tech - Computer Science
    XYZ University
    """
    sections = detect_sections(sample_text)
    
    assert "skills" in sections
    assert "experience" in sections
    assert "education" in sections
    assert "other" in sections # John Doe should be classified as other
    
    assert "Python, Django, SQL" in sections["skills"]
    assert any("ABC Tech - Software Developer" in line for line in sections["experience"])
    assert "XYZ University" in sections["education"]
    assert "John Doe" in sections["other"]
 
def test_section_detection_ignores_keywords_in_sentence():
    # "skills" or "education" inside a full sentence should NOT trigger new sections
    sample_text = """
    SUMMARY
    Experienced machinist with solid manufacturing skills.
    Maintained die logs and tools.
    """
    sections = detect_sections(sample_text)
    assert "skills" not in sections
    assert "summary" in sections
    assert any("Experienced machinist with solid manufacturing skills." in line for line in sections["summary"])

def test_section_detection_heading_variations():
    # Headings wrapped in symbols or with colons
    sample_text = """
    [TECHNICAL SKILLS]
    GD&T, CNC Machining
    * WORK EXPERIENCE *
    Worked at ABC Tool Room.
    """
    sections = detect_sections(sample_text)
    assert "skills" in sections
    assert "experience" in sections
    assert "GD&T, CNC Machining" in sections["skills"]
    assert "Worked at ABC Tool Room." in sections["experience"]

def test_clean_education_section():
    sample_text = """
    EDUCATION
    B.Tech in Computer Science and Engineering 2022 - 2026
    College of Engineering Thalassery, KeralaCGPA: 8.88 10
    Diploma in Tool Die Making 4-Year Course
    NTTF Nettur Technical Training Foundation Graduated 2018
    """
    sections = detect_sections(sample_text)
    assert "education" in sections
    edu = sections["education"]
    assert len(edu) == 4
    assert edu[0] == "B.Tech in Computer Science and Engineering"
    assert edu[1] == "College of Engineering Thalassery, Kerala"
    assert edu[2] == "Diploma in Tool Die Making"
    assert edu[3] == "NTTF Nettur Technical Training Foundation"

