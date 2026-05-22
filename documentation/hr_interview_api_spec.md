# Zecpath HR Interview AI – API Specification

**Base URL**: `https://api.zecpath.ai/v1/hr-interview`

---

## 1. Start Interview
* **Endpoint**: `POST /start`
* **Description**: Initializes a new HR interview session and retrieves initial questions.
* **Request Payload**:
  ```json
  {
    "candidate_id": "C101",
    "job_id": "J501",
    "role_type": "technical",
    "experience_level": "fresher"
  }
  ```
* **Response Payload**:
  ```json
  {
    "session_id": "S123",
    "questions": [
      "Tell me about yourself",
      "What are your strengths?"
    ]
  }
  ```

---

## 2. Submit Answer
* **Endpoint**: `POST /answer`
* **Description**: Submits an answer for the current question and returns adaptive follow-up or the next question.
* **Request Payload**:
  ```json
  {
    "session_id": "S123",
    "question_id": "Q1",
    "answer": "I have experience in Python...",
    "duration": 6
  }
  ```
* **Response Payload**:
  ```json
  {
    "follow_up": "Can you elaborate more?",
    "next_question": "Describe your teamwork experience"
  }
  ```

---

## 3. Get Final Report
* **Endpoint**: `GET /report/{session_id}`
* **Description**: Returns final score breakdown, decision category, and feedback summary.
* **Response Payload**:
  ```json
  {
    "candidate_id": "C101",
    "final_score": 78,
    "decision": "Strong Hire",
    "summary": {
      "strengths": ["Good communication"],
      "weaknesses": ["Minor hesitation"]
    }
  }
  ```

---

## Error Handling Format
```json
{
  "error_code": "INVALID_INPUT",
  "message": "Missing candidate_id",
  "status": 400
}
```
