# Final Recommendation AI – Zecpath

## Objective
To automate final candidate hiring recommendations using a hybrid rule + score risk-adjustment engine.

## Key Features
* **Hybrid rule + score logic**: Applies strict score thresholds while factoring in behavioral indicators and cheating flags.
* **Risk-adjusted scoring**: Adjusts candidate final suitability score with safety penalties based on behavior risk (up to -10) and integrity risk (up to -15).
* **Confidence scoring**: Computes decision confidence based on round-to-round score variance.
* **Explainable outputs**: Automatically details specific candidate strengths (e.g., tech depth, soft skills) and concerns (e.g. behavioral indicators).

## Recommendation Decision Categories

| Category | Threshold | Description |
| --- | --- | --- |
| **Selected** | $\ge 80$ | High performance candidate matching criteria with Low/No risk flags. |
| **Hold / Review** | $60 \dots 79$ | Borderline scores or high-scoring profiles with moderate risk flags. |
| **Rejected** | $< 60$ | Low suitability scores or candidate profiling with high risk indicators. |

---

## Advantages
* **Consistent decisions**: Standardizes evaluation boundaries across recruiters.
* **Integrates risk signals**: Safeguards hiring pipelines by penalizing cheating patterns automatically.
* **Transparent outputs**: Provides immediate explainability notes.

## Limitations
* Rule-based weight deductions and static boundaries.
* Does not factor in external company-specific constraints (e.g., budget limits or timeline pressure).

## Future Improvements
* Recruiter feedback learning loops to optimize thresholds dynamically.
* Adaptive risk weights trained on historic pipeline datasets.
