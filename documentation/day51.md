# Cross-Round Aggregation Engine – Zecpath AI

## Objective
To combine all hiring stages into a single intelligent suitability score.

## Key Features
* **Multi-stage aggregation**: Integrates ATS, Screening, HR Interview, Technical Interview, and Machine Test scores.
* **Role-based weight customization**: Dynamic weighting adjust based on candidate job scopes (e.g. higher technical weights for programmers, higher HR weights for non-technical managers).
* **Hiring fit classification**: Categorizes scores into Excellent, Strong, Moderate, and Low Fit buckets.
* **Explainable scoring**: Clear outputs highlighting how each stage contributed to the final selection decision.

## Stage Weight Distributions

| Stage | Default | Fresher | Experienced | Technical | Non-Technical |
| --- | --- | --- | --- | --- | --- |
| **ATS Match** | 20% | 20% | 25% | 15% | 25% |
| **Screening** | 15% | 20% | 10% | 10% | 20% |
| **HR Interview** | 20% | 25% | 20% | 15% | 35% |
| **Technical** | 25% | 20% | 25% | 35% | 10% |
| **Machine Test** | 20% | 15% | 20% | 25% | 10% |

---

## Advantages
* **Holistic evaluation**: Reduces risk of making hiring decisions based on single-round performance.
* **Fair comparison**: Normalization curves prevent score skewing across different interview pools.
* **Recruiter-friendly**: Translates mathematical scores into straightforward category recommendations.

## Limitations
* Static weight distribution maps require manual updates.
* Lacks adaptive machine learning overrides based on historic hiring patterns.

## Future Improvements
* Dynamic weights auto-optimization using machine learning models.
* Feedback loop integrations tracking recruiter override choices.
