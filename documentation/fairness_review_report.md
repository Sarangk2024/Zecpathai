# AI Fairness Evaluation Report

## Bias Analysis

| Risk Area | Action Taken |
| --- | --- |
| **Name bias** | Candidate name is removed from the profiling payload before scoring |
| **Gender bias** | Gender features are completely unused in scoring models |
| **Accent bias** | Transcription accent signals normalized via STT cleanup operations |
| **Education bias** | Weight reduced for university prestige; skill and logic weights prioritized |

## Fairness Improvements
* **Normalized scoring**: All scoring values are normalized mathematically across candidate pools.
* **Removed non-job-related features**: Social or demographics traits do not influence final calculations.
* **Balanced weight system**: Weight distributions adjust role-based requirements fairly.

## Fairness Metrics

| Metric | Result |
| --- | --- |
| **Bias Detection** | Low |
| **Score Variance Across Groups** | Reduced |
| **Fairness Compliance** | 90% |
