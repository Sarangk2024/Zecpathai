# Zecpath AI Scalability Plan

## 1. Horizontal Service Clusters Scaling
Each service is deployed as a microservice using container orchestration platforms (like Kubernetes or ECS):
* **ATS scoring engine service**: Heavy processing load. Scale automatically when CPU utilization exceeds 70%.
* **Conversational screening service**: Medium scaling profile. Scale based on concurrent active websocket counts.
* **Technical Interview engine service**: High computation profiles. Auto-scale node counts to handle parallel audio transcripts cleaning.
* **Decision calculation engine service**: Low computing load. Standard dual-replica configuration.

---

## 2. Distributed Caching Layer
Use a distributed Redis cluster:
* Cache ATS match score keys.
* Cache candidate profile metadata values.
* Set standard TTL expiration bounds (e.g. 2 hours) to avoid caching outdated scores.

---

## 3. Asynchronous Queue Processing
* For long tasks (e.g. resume document parsing, full evaluation report generation), requests are pushed to a RabbitMQ/Kafka queue.
* Consumer workers pull tasks from queues, execute, update databases, and notify frontend UI pages via webhook endpoints.
