# Unified Scoring Engine – Zecpath AI

## Objective
To combine all hiring stages into a single, intelligent hiring score.

## Unified Scoring Formula
$$Final\ Score = (ATS\ Score \times Weight) + (Screening\ Score \times Weight) + (HR\ Score \times Weight)$$

## Default Weights
| Component | Weight |
| --- | --- |
| **ATS Score** | 30% |
| **Screening Score** | 30% |
| **HR Interview Score** | 40% |

## Role-Based Adjustments
| Candidate Type Profile | ATS Score Weight | Screening Score Weight | HR Interview Weight |
| --- | --- | --- | --- |
| **Fresher** | 25% | 35% | 40% |
| **Experienced** | 35% | 25% | 40% |
| **Technical** | 40% | 30% | 30% |
| **Non-Technical** | 20% | 30% | 50% |

## Advantages
* Holistic evaluation across all hiring rounds.
* Role-based configurable weights allow customization based on role requirements.
* Recruiter-friendly insights via hiring fit categories.

## Limitations
* Static weight limits.
* No machine-learning feedback loop tuning weights dynamically.

## Future Improvements
* ML-based weight optimization.
* Adaptive, historical data-driven scoring models.
