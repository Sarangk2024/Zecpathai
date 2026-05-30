# Performance Tuning & Scalability – Zecpath AI

## Objective
To optimize evaluation response times, lower CPU/memory usage footprint, and define horizontal auto-scaling guidelines.

## Key Enhancements
* **Inference caching**: Caching repeated score requests using `@lru_cache` decorators to skip redundant computations.
* **Streaming data processing**: Utilizing generator streams (`yield`) to process applicant data chunks one-by-one, minimizing heap allocations.
* **Batch processing**: Grouping resume ingest operations into concurrent batches.
* **horizontal scaling designs**: Utilizing containers (Docker, Kubernetes) and load balancers to scale microservices nodes dynamically.

---

## Advantages
* **Optimized Latency**: Cache hits return results in microseconds.
* **Low Infrastructure Costs**: Memory optimization limits RAM leaks under heavy candidate volumes.
* **Enterprise-grade throughput**: Prepared to auto-scale dynamically.

## Limitations
* In-memory cache sizes are bounded by RAM constraints.
* Distributed cache sync protocols require dedicated Redis/Memcached infrastructures.

## Future Improvements
* GPU acceleration pipelines for voice-to-text audio transcriptions.
* Edge AI local inferences.
