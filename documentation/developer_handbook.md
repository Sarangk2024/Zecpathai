# HR Interview AI Developer Handbook – Zecpath

## Contents
* Architecture Overview
* API Reference
* Data Models
* Scoring Logic
* Integration Steps
* Troubleshooting Guide

---

## Advantages
* **Easy integration**: Standard HTTP REST JSON requests and responses.
* **Scalable system**: Modular design allows running engines independently.
* **Clear documentation**: Complete request payloads and schema specifications.

## Limitations
* Requires backend orchestrator support.
* Includes rule-based fallback components.

## Future Improvements
* Client-side SDK for developers (JS/Python/Go).
* GraphQL API interfaces.
* Real-time audio streaming websockets API.

---

## Developer Integration Guide

### Steps to Integrate
1. Call the `/start` API to initialize a candidate session.
2. Receive interview questions for the role.
3. Capture the candidate's responses (verbal audio or text).
4. Send the answers via the `/answer` API.
5. Repeat for subsequent questions until the interview concludes.
6. Call the `/report` API to retrieve the final hiring recommendation report.
7. Display the results in the recruiter dashboard.

### Tech Stack
* **Backend**: Python (Flask/FastAPI)
* **AI Engine**: NLP + Rule-based + ML (PyTorch/Scikit-Learn)
* **Database**: PostgreSQL / MongoDB

---

## Troubleshooting Guide

### Common Issues & Fixes

| Issue | Solution |
| --- | --- |
| **No response detected** | Retry Speech-to-Text conversion |
| **Low score anomaly** | Verify normalization factors and input boundaries |
| **API timeout** | Increase server-side timeouts / implement retry limits |
| **Wrong intent detection** | Improve keyword matches or threshold classifier parameters |

### Debug Checklist
* [ ] API logs verified and error logs cleared
* [ ] Input candidate profiles validated
* [ ] Model confidence scores checked
* [ ] Scoring outputs within [0, 100] range
* [ ] No missing fields in JSON report payloads
