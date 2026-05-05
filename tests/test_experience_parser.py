# tests/test_experience_parser.py - Unit tests for experience parsing & relevance.

import pytest
from ats_engine.experience_parser import (
    extract_experience_blocks, extract_roles, calculate_total_experience,
    detect_gaps, detect_overlaps, calculate_relevance
)

def test_extract_experience_blocks():
    text = """
    ABC Tech (2021-2024)
    Software Developer
    XYZ Solutions (2018-2020)
    Intern
    """
    experiences = extract_experience_blocks(text)
    assert len(experiences) == 2
    assert experiences[0]["company"] == "ABC Tech"
    assert experiences[0]["start_year"] == 2021
    assert experiences[0]["end_year"] == 2024
    assert experiences[0]["duration_years"] == 3
    
    assert experiences[1]["company"] == "XYZ Solutions"
    assert experiences[1]["start_year"] == 2018
    assert experiences[1]["end_year"] == 2020
    assert experiences[1]["duration_years"] == 2

def test_extract_experience_present():
    text = "Work at ABC Corp (2022-Present)"
    experiences = extract_experience_blocks(text)
    assert len(experiences) == 1
    assert experiences[0]["company"] == "Work at ABC Corp"
    assert experiences[0]["end_year"] == 2026 # 2026 is the mock year in current local time metadata

def test_calculate_total_experience():
    exps = [
        {"company": "A", "duration_years": 3},
        {"company": "B", "duration_years": 2}
    ]
    assert calculate_total_experience(exps) == 5

def test_detect_gaps():
    exps = [
        {"company": "A", "start_year": 2018, "end_year": 2020},
        {"company": "B", "start_year": 2022, "end_year": 2025}
    ]
    gaps = detect_gaps(exps)
    assert len(gaps) == 1
    assert gaps[0]["gap_years"] == 2
    assert gaps[0]["between"] == "2020 - 2022"

def test_detect_overlaps():
    exps = [
        {"company": "A", "start_year": 2018, "end_year": 2021},
        {"company": "B", "start_year": 2020, "end_year": 2023}
    ]
    overlaps = detect_overlaps(exps)
    assert len(overlaps) == 1
    assert overlaps[0][0]["company"] == "A"
    assert overlaps[0][1]["company"] == "B"

def test_extract_roles():
    text = "CNC Machinist at ABC Tech. Formerly worked as Tool Maker."
    roles = extract_roles(text)
    assert "cnc machinist" in roles
    assert "tool maker" in roles
    assert "machinist" in roles

def test_calculate_relevance():
    candidate_roles = ["cnc machinist", "tool maker"]
    assert calculate_relevance(candidate_roles, "tool maker") == 85.0 # Exact match 1.0, trade family similarity 0.7 -> average is (1.0 + 0.7)/2 = 85.0%
    assert calculate_relevance(candidate_roles, "developer") == 0.0

def test_extract_experience_blocks_robust():
    text = """
    Software Developer Intern Eqsoft Business Solutions Pvt Ltd Jun 2025 Jul 2025
    Senior Die Maker - Escorts Auto Component Division 2020 - Present
    """
    experiences = extract_experience_blocks(text)
    assert len(experiences) == 2
    assert experiences[0]["company"] == "Software Developer Intern Eqsoft Business Solutions Pvt Ltd"
    assert experiences[0]["start_year"] == 2025
    assert experiences[0]["end_year"] == 2025
    assert experiences[0]["duration_years"] == 0
    assert experiences[0]["duration_months"] == 1
    assert experiences[0]["start_month"] == 6
    assert experiences[0]["end_month"] == 7
    
    assert experiences[1]["company"] == "Senior Die Maker - Escorts Auto Component Division"
    assert experiences[1]["start_year"] == 2020
    assert experiences[1]["end_year"] == 2026
    
def test_detect_gaps_months():
    exps = [
        {"company": "A", "start_year": 2025, "start_month": 6, "start_month_idx": 24306, "end_year": 2025, "end_month": 7, "end_month_idx": 24307, "duration_months": 1},
        {"company": "B", "start_year": 2025, "start_month": 12, "start_month_idx": 24312, "end_year": 2026, "end_month": 3, "end_month_idx": 24315, "duration_months": 3}
    ]
    gaps = detect_gaps(exps)
    assert len(gaps) == 1
    assert gaps[0]["gap_months"] == 4
    assert gaps[0]["between"] == "Jul 2025 - Dec 2025"

def test_detect_overlaps_months():
    exps_non_overlapping = [
        {"company": "A", "start_year": 2025, "start_month": 6, "start_month_idx": 24306, "end_year": 2025, "end_month": 7, "end_month_idx": 24307},
        {"company": "B", "start_year": 2025, "start_month": 12, "start_month_idx": 24312, "end_year": 2026, "end_month": 3, "end_month_idx": 24315}
    ]
    overlaps_none = detect_overlaps(exps_non_overlapping)
    assert len(overlaps_none) == 0

    exps_overlapping = [
        {"company": "A", "start_year": 2025, "start_month": 6, "start_month_idx": 24306, "end_year": 2025, "end_month": 12, "end_month_idx": 24312},
        {"company": "B", "start_year": 2025, "start_month": 10, "start_month_idx": 24310, "end_year": 2026, "end_month": 3, "end_month_idx": 24315}
    ]
    overlaps_some = detect_overlaps(exps_overlapping)
    assert len(overlaps_some) == 1
    assert overlaps_some[0][0]["company"] == "A"
    assert overlaps_some[0][1]["company"] == "B"

def test_calculate_relevance_dilution():
    candidate_roles = ["developer", "software developer", "intern"]
    # Intern should be filtered out, developer is exact (1.0), software developer matches developer word (1.0).
    # Expected: 2.0 / 2 = 100%
    relevance = calculate_relevance(candidate_roles, "developer")
    assert relevance == 100.0
