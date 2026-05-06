# tests/test_education_parser.py - Unit tests for education and certification parsing.

from parsers.education_parser import (
    extract_education, extract_certifications, 
    calculate_education_relevance, calculate_certification_relevance
)

def test_education():
    text = "B.Tech 2021"
    result = extract_education(text)
    assert len(result) > 0
    assert result[0]["degree"] == "B.Tech"
    assert result[0]["year_of_completion"] == "2021"

def test_education_robust():
    text = "B.Tech in Computer Science from XYZ University (2021)"
    result = extract_education(text)
    assert len(result) == 1
    assert result[0]["degree"] == "B.Tech"
    assert result[0]["field"] == "Computer Science"
    assert result[0]["institution"] == "XYZ University"
    assert result[0]["year_of_completion"] == "2021"

def test_education_manufacturing():
    text = "Diploma in Mechanical Engineering from State Board Completed 2020"
    result = extract_education(text)
    assert len(result) == 1
    assert result[0]["degree"] == "Diploma"
    assert result[0]["field"] in ["Mechanical", "Mechanical Engineering"]
    assert result[0]["year_of_completion"] == "2020"

def test_extract_certifications():
    text = """
    AWS Certified Developer
    Certified in SolidWorks
    """
    certs = extract_certifications(text)
    assert len(certs) == 2
    assert certs[0]["category"] == "Cloud"
    assert certs[1]["category"] == "CAD_CAM"

def test_calculate_education_relevance():
    assert calculate_education_relevance("B.Tech", "B.Tech") == 1.0
    assert calculate_education_relevance("M.Tech", "B.Tech") == 0.8
    assert calculate_education_relevance("B.Tech", "Diploma") == 0.9
    assert calculate_education_relevance("Diploma", "B.Tech") == 0.5

def test_calculate_certification_relevance():
    certs = [
        {"name": "AWS Certified Developer", "category": "Cloud"},
        {"name": "SolidWorks Certified", "category": "CAD_CAM"}
    ]
    job_skills = ["Cloud", "Python"]
    assert calculate_certification_relevance(certs, job_skills) == 50.0

def test_education_multiline():
    text = "B.E. in Mechanical Engineering\nCollege of Engineering, Guindy Graduated 2018"
    result = extract_education(text)
    assert len(result) == 1
    assert result[0]["degree"] == "B.Tech"
    assert result[0]["field"] == "Mechanical Engineering"
    assert result[0]["institution"] == "College of Engineering, Guindy"
    assert result[0]["year_of_completion"] == "2018"
