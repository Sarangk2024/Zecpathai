# Technical Interview AI Design – Zecpath

## Objective
To build an adaptive AI system for evaluating technical skills.

## Key Features
* **Role-based questioning**: Dynamic mapping of applicant's target role to skill topics.
* **Experience-based difficulty**: Segmenting initial questions by candidate years of experience.
* **Dynamic progression**: Adjusting question difficulty level on the fly based on answer quality.
* **Technical scoring**: Evaluates logical correctness and real-world applicability.

## Question Categories

| Type | Description |
| --- | --- |
| **Conceptual** | Theory-based questions explaining frameworks and basic concepts |
| **Coding** | Problem-solving questions testing logic and coding capability |
| **Scenario** | Real-world problem scenarios requiring logic-based decisions |
| **System Design** | Architecture decisions and scalability problem questions |

---

## Advantages
* **Personalized interviews**: Tailored difficulty bounds prevent candidates from feeling overwhelmed or under-challenged.
* **Scalable evaluation**: Automated questioning and routing logic.
* **Real-world relevance**: Promotes scenario and system design evaluations for seniors.

## Limitations
* Rule-based transitions engine.
* Does not execute candidate code inside the baseline query generator.

## Future Improvements
* Sandbox code execution runner integrations.
* LLM-based semantic reasoning feedback.
* Real-time automated typing speed tracker.
