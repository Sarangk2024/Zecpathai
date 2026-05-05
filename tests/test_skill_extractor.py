# tests/test_skill_extractor.py - Unit tests for skill extraction engine.

import pytest
from ats_engine.skill_extractor import (
    clean_text, extract_skills, calculate_confidence, extract_skills_with_confidence
)

def test_clean_text():
    raw = "CNC Machinist with SolidWorks & AutoCAD! @ Pune"
    expected = "cnc machinist with solidworks  autocad  pune"
    assert clean_text(raw) == expected

def test_extract_skills():
    text = "Developer with experience in py, Django and js. Knowledge of GD&T."
    skills = extract_skills(text)
    assert "python" in skills
    assert "django" in skills
    assert "javascript" in skills
    assert "gd_t" in skills
    assert "react" not in skills

def test_extract_skills_stack_expansion():
    text = "We built this project using the MERN stack."
    skills = extract_skills(text)
    assert "mongodb" in skills
    assert "express" in skills
    assert "react" in skills
    assert "node" in skills

def test_calculate_confidence():
    text = """
    We need python developer.
    Python is the main language.
    All models are written in python.
    """
    assert calculate_confidence("python", text) == 0.95
    assert calculate_confidence("django", text) == 0.0

def test_extract_skills_with_confidence():
    text = "Python developer. We use python and django."
    res = extract_skills_with_confidence(text)
    
    python_entry = next((item for item in res if item["skill"] == "python"), None)
    django_entry = next((item for item in res if item["skill"] == "django"), None)
    
    assert python_entry is not None
    assert django_entry is not None
    assert python_entry["confidence"] == 0.85 # two occurrences
    assert django_entry["confidence"] == 0.75 # one occurrence
