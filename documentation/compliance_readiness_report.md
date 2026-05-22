# AI Compliance Readiness – Zecpath

## Data Retention Policy
* Candidate data is stored securely for a maximum of 90 days.
* After 90 days, candidate data is either automatically anonymized or permanently deleted.
* Recruiters or candidates can request immediate deletion at any time.

## Compliance Standards Alignment

| Standard | Status |
| --- | --- |
| **GDPR (General Data Protection Regulation)** | Partial alignment |
| **Data Minimization** | Implemented (only job-relevant questions and answers kept) |
| **Consent Management** | Implemented (explicit candidate consent required before starting) |
| **Right to Erasure** | Supported (manual and automatic cleanup flows available) |

## Security Measures
* **Encrypted storage**: Candidates' stored profiles and text transcripts are encrypted at rest.
* **Secure API endpoints**: Role-based access controls and token validation on all resources.
* **Access logging**: System audit trails log every recruiter interaction with evaluations.

## Risk Assessment

| Risk | Mitigation |
| --- | --- |
| **Bias risk** | Periodic fairness checks and automated validation checks |
| **Data misuse** | Role-based access control filters |
| **Model errors** | Human review override option for all hiring recommendations |
