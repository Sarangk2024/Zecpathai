# Optimization & Refinement – Zecpath AI

## Objective
To improve system accuracy, reduce false positives and negatives, and refine candidate intent classification.

## Key Enhancements
* **Threshold tuning**: Adjusting Selected threshold (from 80 to 78) and Hold threshold (from 60 to 58) to balance precision and recall.
* **Consistency-based scoring**: Adjusting candidate final scores by penalizing large cross-round score variances (variance $>30 \implies -5$) and rewarding consistent performance across stages (variance $<10 \implies +5$).
* **Refined intent detection**: Enhancing keyword mapping to accurately categorize dialogue intents (experience, education, future intent, generic).
* **Speed optimization**: Introducing optimized batch execution wrappers.

---

## Advantages
* **Optimized selection decisions**: Edge case checks correct false recommendations.
* **Reduced errors**: Score adjustments penalize suspicious score fluctuations.
* **Refined candidate insights**: More accurate dialogue parsing.

## Limitations
* Rules-based adjustments require continuous validation against actual hiring patterns.
* Still lacks machine learning models to identify anomalies.

## Future Improvements
* Dynamic thresholds using auto-learning models.
* Feedback loop interfaces to update keyword lists automatically.
