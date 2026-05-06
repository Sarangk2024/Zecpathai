# tests/test_semantic_matcher.py - Unit tests for semantic matching engine.

from ats_engine.semantic_matcher import compute_similarity, match_resume_to_jd, classify_match

def test_similarity():
    text1 = "Python developer"
    text2 = "Backend engineer using Python"
    score = compute_similarity(text1, text2)
    assert score > 0.5

def test_match_resume_to_jd():
    resume = {
        "skills": ["Python", "Django", "REST API"],
        "experience": [{"role": "Backend Developer"}],
        "projects": [{"description": "Built scalable REST APIs using Django"}]
    }
    jd = {
        "job_title": "Backend Developer",
        "required_skills": ["Python", "Django", "API"],
        "job_description_text": "Looking for backend developer to build APIs and scalable systems"
    }
    result = match_resume_to_jd(resume, jd)
    assert "skills_similarity" in result
    assert "experience_similarity" in result
    assert "project_similarity" in result
    assert result["final_similarity_score"] > 0

def test_classify_match():
    assert classify_match(90) == "Strong Match"
    assert classify_match(60) == "Moderate Match"
    assert classify_match(40) == "Weak Match"
