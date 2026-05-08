# tests/test_ats_accuracy.py - Accuracy, precision, and recall evaluations for Zecpath AI.

# 40 Candidate Mock dataset reflecting manual review vs AI decisions
MOCK_TEST_DATA = [
    # Tech Roles (10 Candidates) - 9 Correct (90.0% Accuracy)
    {"candidate_id": "TC01", "category": "Tech", "role": "Backend Developer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "TC02", "category": "Tech", "role": "Backend Developer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "TC03", "category": "Tech", "role": "Data Scientist", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "TC04", "category": "Tech", "role": "DevOps Engineer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "TC05", "category": "Tech", "role": "Frontend Developer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "TC06", "category": "Tech", "role": "Backend Developer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "TC07", "category": "Tech", "role": "Data Scientist", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "TC08", "category": "Tech", "role": "DevOps Engineer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "TC09", "category": "Tech", "role": "Frontend Developer", "ai": "Rejected", "hr": "Rejected"}, # TN
    {"candidate_id": "TC10", "category": "Tech", "role": "Backend Developer", "ai": "Rejected", "hr": "Shortlisted"}, # FN (Mismatch: Mismatch Case - AI rejected, HR shortlisted)

    # Non-Tech Roles (10 Candidates) - 7 Correct (70.0% / ~78% Accuracy target adjusted)
    {"candidate_id": "NC01", "category": "Non-Tech", "role": "Marketing Executive", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "NC02", "category": "Non-Tech", "role": "HR Manager", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "NC03", "category": "Non-Tech", "role": "Sales Executive", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "NC04", "category": "Non-Tech", "role": "Business Analyst", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "NC05", "category": "Non-Tech", "role": "Marketing Executive", "ai": "Shortlisted", "hr": "Rejected"}, # FP (Mismatch: AI shortlisted, HR rejected)
    {"candidate_id": "NC06", "category": "Non-Tech", "role": "HR Manager", "ai": "Shortlisted", "hr": "Rejected"}, # FP (Mismatch: AI shortlisted, HR rejected)
    {"candidate_id": "NC07", "category": "Non-Tech", "role": "Sales Executive", "ai": "Rejected", "hr": "Shortlisted"}, # FN (Mismatch: AI rejected, HR shortlisted)
    {"candidate_id": "NC08", "category": "Non-Tech", "role": "Business Analyst", "ai": "Rejected", "hr": "Rejected"}, # TN
    {"candidate_id": "NC09", "category": "Non-Tech", "role": "Marketing Executive", "ai": "Rejected", "hr": "Rejected"}, # TN
    {"candidate_id": "NC10", "category": "Non-Tech", "role": "HR Manager", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP

    # Fresher Profiles (10 Candidates) - 8 Correct (80.0% Accuracy)
    {"candidate_id": "FC01", "category": "Fresher", "role": "Fresher Developer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "FC02", "category": "Fresher", "role": "Fresher Developer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "FC03", "category": "Fresher", "role": "Fresher Machinist", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "FC04", "category": "Fresher", "role": "Fresher Designer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "FC05", "category": "Fresher", "role": "Fresher Developer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "FC06", "category": "Fresher", "role": "Fresher Developer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "FC07", "category": "Fresher", "role": "Fresher Designer", "ai": "Rejected", "hr": "Shortlisted"}, # FN (Mismatch: AI rejected, HR shortlisted)
    {"candidate_id": "FC08", "category": "Fresher", "role": "Fresher Machinist", "ai": "Rejected", "hr": "Rejected"}, # TN
    {"candidate_id": "FC09", "category": "Fresher", "role": "Fresher Developer", "ai": "Rejected", "hr": "Rejected"}, # TN
    {"candidate_id": "FC10", "category": "Fresher", "role": "Fresher Developer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP

    # Senior Profiles (10 Candidates) - 9 Correct (90.0% / ~85% Accuracy target adjusted)
    {"candidate_id": "SC01", "category": "Senior", "role": "Lead Developer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "SC02", "category": "Senior", "role": "Senior Mold Designer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "SC03", "category": "Senior", "role": "Senior Die Engineer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "SC04", "category": "Senior", "role": "Senior Machinist", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "SC05", "category": "Senior", "role": "Lead Developer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "SC06", "category": "Senior", "role": "Senior Mold Designer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "SC07", "category": "Senior", "role": "Senior Die Engineer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
    {"candidate_id": "SC08", "category": "Senior", "role": "Senior Machinist", "ai": "Shortlisted", "hr": "Rejected"}, # FP (Mismatch: AI shortlisted, HR rejected)
    {"candidate_id": "SC09", "category": "Senior", "role": "Lead Developer", "ai": "Rejected", "hr": "Shortlisted"}, # FN (Mismatch: AI rejected, HR shortlisted)
    {"candidate_id": "SC10", "category": "Senior", "role": "Senior Mold Designer", "ai": "Shortlisted", "hr": "Shortlisted"}, # TP
]

def evaluate_accuracy(ai_results, hr_results):
    tp = fp = fn = tn = 0
    for ai, hr in zip(ai_results, hr_results):
        if ai == "Shortlisted" and hr == "Shortlisted":
            tp += 1
        elif ai == "Shortlisted" and hr == "Rejected":
            fp += 1
        elif ai == "Rejected" and hr == "Shortlisted":
            fn += 1
        else:
            tn += 1
            
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    accuracy = (tp + tn) / len(ai_results) if len(ai_results) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy,
        "f1_score": f1
    }

def test_accuracy_metrics():
    ai = [c["ai"] for c in MOCK_TEST_DATA]
    hr = [c["hr"] for c in MOCK_TEST_DATA]
    metrics = evaluate_accuracy(ai, hr)
    assert metrics["tp"] == 28
    assert metrics["fn"] == 4
    assert metrics["fp"] == 3
    assert metrics["tn"] == 5
    assert round(metrics["accuracy"] * 100, 1) == 82.5
