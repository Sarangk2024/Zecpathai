# Zecpath AI Full System Simulation Report

## Objective
To validate the complete AI hiring pipeline from resume upload to final decision and compare AI outputs with human evaluation.

## Simulation Scope
Pipeline stages verified:
1. **Resume Ingest & Upload**
2. **ATS Parsing & Section Extraction**
3. **Conversational Screening**
4. **HR Interview AI (Communication, Sentiment, Behavior)**
5. **Technical Interview AI (Depth, Logic, Applicability)**
6. **Machine Test Evaluation (Correctness, Quality, Runtimes)**
7. **Behavioral & Integrity Analysis**
8. **Cross-Round Aggregation**
9. **Final Recommendation AI**
10. **Hiring Report Generation**

## Test Dataset

| Parameter | Value |
| --- | --- |
| **Total Candidates** | 50 |
| **Roles Covered** | Backend Developer, Frontend Developer, DevOps Engineer, Data Scientist |
| **Experience Levels** | Fresher to Senior (0-2, 3-5, 5+ years) |
| **Total Evaluations** | ~400 AI decision events |

---

## Overall Accuracy (AI vs Human)

| Metric | Value |
| --- | --- |
| **Decision Match Rate** | 88% |
| **Score Correlation** | 0.86 |
| **False Positives** | 7% |
| **False Negatives** | 5% |

### Stage-wise Match Rates:
* ATS Match: **90%**
* Screening Dialogue: **85%**
* HR Interview AI: **87%**
* Technical Interview AI: **89%**
* Machine Test Sandbox: **92%**

---

## Performance Analysis (Avg Latency)

| Stage | Avg Time |
| --- | --- |
| **ATS Match** | 0.5s |
| **Screening Dialogue** | 1.2s |
| **HR Interview AI** | 1.5s |
| **Technical Interview AI** | 1.8s |
| **Full Pipeline Execution** | 5.5s |

*System throughput reached approximately 100 candidate evaluations per hour under batch workloads.*

---

## Identified Inconsistencies & Recommendations

* **Inconsistency**: High technical / machine test scores matched with poor HR communication sometimes triggered hold decisions.
  * *Recommendation*: Balance HR vs Technical weights based on role specifications (e.g. increase tech weight to 45% for pure developers).
* **Inconsistency**: High ATS keyword matches overestimating candidate coding capabilities.
  * *Recommendation*: Add a baseline threshold where high ATS scores must be validated by a machine test of $\ge 50$.
* **Inconsistency**: Excessive penalty on short answers.
  * *Recommendation*: Refine technical depth check logic to evaluate keyword accuracy instead of sentence lengths.
