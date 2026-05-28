# Zecpath AI Compliance & Governance Design

## Objective
To ensure the AI system is secure, auditable, privacy-compliant, and aligned with ethical data usage standards.

## Core Principles
* **Consent-first data processing**
* **Auditability of all AI decisions**
* **Secure storage & transmission**
* **Role-based access control (RBAC)**
* **Data minimization & retention policies**

---

## Consent-Based Data Usage
Before initializing an automated video screening session, the candidate must explicitly agree to the following checkpoints:
* **AI Evaluation**: The candidate consents to have their responses rated by the AI models.
* **Recording**: The candidate accepts audio/video captures.
* **Data Processing**: The candidate agrees to securely store their parsed profile and scores.

*Note: All candidate approvals are logged with a timestamp and linked directly to their Candidate ID.*

---

## Data Retention Policy

| Data Type | Retention Limit | Action After Expiration |
| --- | --- | --- |
| **Resume Data** | 90 days | Auto-delete file and clean parsed profile indices |
| **Interview Transcripts** | 60 days | Permanently scrub dialogues and text sheets |
| **Reports & Scores** | 120 days | Anonymize candidate identifiers |
| **Audit Logs** | 180 days | Archive to secure cold storage |

---

## AI Security Architecture – Zecpath

### System Architecture
```
User / Candidate
       ↓
Secure API Gateway (HTTPS / Rate Limited)
       ↓
Authentication Layer (JWT / OAuth token check)
       ↓
Authorization Layer (RBAC check via security/access_control.py)
       ↓
AI Processing Services
       ↓
Encrypted Database Storage (using AES-256)
       ↓
Audit Logging System (Write-only event tracker)
```

---

## Audit Trail Logs

| Log Type | Description |
| --- | --- |
| **Score Logs** | Traces weight factors and outputs for each round |
| **Decision Logs** | Captures final recommendation and risk penalties |
| **Access Logs** | Traces recruiter token access metadata |
| **Consent Logs** | Stores candidate consent ticks |
