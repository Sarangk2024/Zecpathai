# tests/test_resume_extractor.py - Unit tests for Zecpath AI resume text extraction.

import pytest
from parsers.resume_extractor import clean_text, normalize_sections

def test_clean_text_normalizes_bullets():
    """
    Check that bullet variations are standardized to a simple hyphen.
    """
    raw_input = "● Worked with CNC Lathes\n• Maintained tool room templates\n▪ Designed progressive dies"
    expected = "- Worked with CNC Lathes\n - Maintained tool room templates\n - Designed progressive dies"
    
    assert clean_text(raw_input) == expected

def test_clean_text_strips_special_characters():
    """
    Check that random special symbols are dropped while standard alphanumeric text is kept.
    """
    raw_input = "John Doe #$^*()[]{} - Tool & Die Maker! @ Pune"
    expected = "John Doe - Tool Die Maker @ Pune"
    
    assert clean_text(raw_input) == expected

def test_clean_text_normalizes_multiple_spaces():
    """
    Verify that double/triple inline spacing is compressed.
    """
    raw_input = "Machinist     with    5    years    experience"
    expected = "Machinist with 5 years experience"
    
    assert clean_text(raw_input) == expected

def test_normalize_sections_standardizes_headings():
    """
    Check that common section headings are standardized.
    """
    raw_input = "WORK EXPERIENCE ABC Manufacturing SKILLS SET G-Code, GD&T EDUCATION DETAILS ITI Diploma"
    expected = "Experience ABC Manufacturing Skills G-Code, GD&T Education ITI Diploma"
    
    assert normalize_sections(raw_input) == expected

def test_clean_text_handles_empty_input():
    """
    Verify empty input edge case returns empty string.
    """
    assert clean_text("") == ""
    assert clean_text(None) == ""
