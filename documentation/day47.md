# Technical Skill Scoring Model – Zecpath AI

## Objective
To evaluate technical depth and real-world understanding.

## Key Parameters

| Parameter | Description |
| --- | --- |
| **Accuracy** | Correctness of the technical concept or solution |
| **Depth** | Explanation quality, presence of architecture, scaling, optimization keywords |
| **Logic** | Reasoning quality, structure of explanation (e.g. chronological orders) |
| **Real-world** | Practical relevance, production context, example usage |

---

## Advantages
* **Deep evaluation beyond keywords**: Scores structured logic and explanation depth, not just exact match labels.
* **Structured scoring**: Applies specific rubrics per question type.
* **Explainable outputs**: Breaks down ratings across accuracy, depth, logic, and applicability for recruiter review.

## Limitations
* Rule-based keyword checks.
* No compile-time execution of code logic in the scoring engine.

## Future Improvements
* Abstract Syntax Tree (AST) code structure evaluator integrations.
* LLM-based reasoning and logic analysis.
* Plagiarism checks compared against web queries.
