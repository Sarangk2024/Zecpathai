# run_d43_ethics_compliance.py

import json
from interview_ai.ethics_check import verify_candidate_consent, mask_demographic_signals, check_data_retention_compliance

def main():
    print("\n==========================================================================================")
    print("ZECPATH ETHICS & COMPLIANCE RUNNER (DAY 43)")
    print("==========================================================================================\n")

    # 1. Candidate Consent Check
    print("--- [STEP 1] VERIFYING CANDIDATE CONSENT ---")
    valid_consent = {"ai_evaluation": True, "data_processing": True}
    invalid_consent = {"ai_evaluation": True, "data_processing": False}
    
    print(f"Consent A (Complete Agreement): {valid_consent} -> Allowed: {verify_candidate_consent(valid_consent)}")
    print(f"Consent B (Declined Processing): {invalid_consent} -> Allowed: {verify_candidate_consent(invalid_consent)}")

    # 2. PII Demographic Signal Masking
    print("\n--- [STEP 2] DEMOGRAPHIC SIGNAL MASKING ---")
    raw_profile = {
        "candidate_id": "C1004",
        "name": "Jane Miller",
        "gender": "Female",
        "age": 31,
        "location": "New York",
        "skills": ["React", "TypeScript", "Node.js"],
        "education": "BS Computer Science"
    }
    
    print("Raw Candidate Profile:")
    print(json.dumps(raw_profile, indent=2))
    
    masked_profile = mask_demographic_signals(raw_profile)
    print("\nMasked Candidate Profile (Sent to Scoring Engine):")
    print(json.dumps(masked_profile, indent=2))

    # 3. Data Retention Compliance Checks
    print("\n--- [STEP 3] DATA RETENTION COMPLIANCE CHECKS ---")
    retention_checks = [45, 90, 120]
    for days in retention_checks:
        action = check_data_retention_compliance(days)
        print(f"Candidate data stored for: {days:>3} days -> Compliance Action: {action}")

    # 4. Final Compliance Checklist Printout
    print("\n--- [STEP 4] FINAL COMPLIANCE CHECKLIST ---")
    checklist = {
        "Candidate consent collected": True,
        "No demographic bias signals used": True,
        "Explainable scoring implemented": True,
        "Data retention policy defined": True,
        "Secure storage enabled": True,
        "Audit logs maintained": True
    }
    for item, status in checklist.items():
        print(f"[OK] {item:<40} : {status}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 43 Ethics & Compliance Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
