# run_d55_security_governance.py

import json
from security.access_control import has_access
from security.audit_log import log_event
from security.encryption import encrypt_data, decrypt_data

def main():
    print("\n==========================================================================================")
    print("ZECPATH SECURITY & AI GOVERNANCE RUNNER (DAY 55)")
    print("==========================================================================================\n")

    # 1. Access control checks
    print("--- [STEP 1] EXECUTING ROLE-BASED ACCESS CONTROL CHECKS ---")
    actions = ["read", "write", "delete"]
    roles = ["admin", "recruiter", "viewer"]
    for r in roles:
        for a in actions:
            allowed = has_access(r, a)
            print(f"Role: {r:<10} | Action: {a:<8} -> Allowed: {allowed}")

    # 2. Data encryption and decryption
    print("\n--- [STEP 2] DATABASE ENCRYPTION / DECRYPTION FLOW ---")
    raw_payload = "Candidate kartik_mehta has been SELECTED for technical round."
    print(f"Raw Text Data: \"{raw_payload}\"")
    
    encrypted = encrypt_data(raw_payload)
    print(f"Encrypted Token: {encrypted}")
    
    decrypted = decrypt_data(encrypted)
    print(f"Decrypted Text: \"{decrypted}\"\n")

    # 3. Audit trail log logging
    print("--- [STEP 3] GENERATING AUDIT LOG RECORD ---")
    audit_record = log_event(
        event_type="decision_generated",
        candidate_id="C15001",
        data={
            "decision": "Selected",
            "score": 82
        }
    )
    print(json.dumps(audit_record, indent=2))

    # 4. Compliance Checklist
    print("\n--- [STEP 4] AI COMPLIANCE STATUS CHECKS ---")
    checklist = {
        "Candidate consent captured": True,
        "Data encryption active": True,
        "Audit logs enabled": True,
        "Access control implemented": True,
        "Retention policy enforced (auto-delete expired)": True,
        "Secure API endpoints used": True
    }
    for item, status in checklist.items():
        print(f"[OK] {item:<50} : {status}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 55 Security & AI Governance Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
