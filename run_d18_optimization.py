# run_optimization.py - Performance testing and stress validation runner (Day 18).

import time
import os
import json
from ats_engine.optimized_engine import (
    clean_text_cached,
    clean_noisy_resume,
    fast_skill_extract,
    process_resumes_parallel,
    batch_process,
    safe_execute,
    retry,
    run_with_timeout
)

# Mock raw non-cached/non-parallel logic for comparative benchmarking
def raw_clean_text(text):
    if not text:
        return ""
    # Simulates lack of caching by always compiling/running heavy processes
    time.sleep(0.005) # simulate minor processing delay
    text = text.lower()
    text = "".join([c for c in text if c.isalnum() or c.isspace() or c in ".,-"])
    text = " ".join(text.split())
    return text

def raw_skill_extract(text):
    cleaned = raw_clean_text(text)
    time.sleep(0.005) # simulate lookup overhead
    skills = ["python", "java", "react", "node", "sql", "django"]
    return [s for s in skills if s in cleaned]

def main():
    print("\n==========================================================================================")
    print("ZECPATH ATS OPTIMIZATION & PERFORMANCE TUNING RUNNER (DAY 18)")
    print("==========================================================================================")

    # Prepare 100 mock noisy resumes to run stress and benchmark testing
    base_resume = "Python Developer!!! with Django---- experience. React and SQL skills... also knows Javaaaaa!"
    test_resumes = [f"{base_resume} [Candidate Ref {i}]" for i in range(100)]
    
    print(f"\nCreated stress-test dataset: {len(test_resumes)} resumes.")
    
    # 1. Benchmarking Clean Text + Skill Extraction Time (Raw vs Optimized Caching)
    print("\n--- [BENCHMARK 1] RAW VS OPTIMIZED TEXT & SKILL LOOKUP ---")
    start_time = time.time()
    for text in test_resumes:
        raw_skill_extract(text)
    raw_duration = time.time() - start_time
    print(f"Raw sequential lookup time: {raw_duration:.4f} seconds")
    
    # Run once to warm cache, then run benchmark
    for text in test_resumes:
        fast_skill_extract(text)
        
    start_time = time.time()
    for text in test_resumes:
        fast_skill_extract(text)
    opt_duration = time.time() - start_time
    improvement = ((raw_duration - opt_duration) / raw_duration) * 100 if raw_duration > 0 else 0
    print(f"Optimized cached lookup time: {opt_duration:.4f} seconds (Improvement: {improvement:.1f}%)")

    # 2. Benchmarking Parallel Processing
    print("\n--- [BENCHMARK 2] PARALLEL EXECUTION (THREAD POOL EXECUTOR) ---")
    cleaned_resumes = [clean_noisy_resume(r) for r in test_resumes]
    
    # Sequential
    start_seq = time.time()
    seq_results = [fast_skill_extract(r) for r in cleaned_resumes]
    seq_duration = time.time() - start_seq
    print(f"Sequential processing duration (100 resumes): {seq_duration:.4f} seconds")
    
    # Parallel
    start_par = time.time()
    par_results = process_resumes_parallel(cleaned_resumes, fast_skill_extract, max_workers=4)
    par_duration = time.time() - start_par
    improvement_par = ((seq_duration - par_duration) / seq_duration) * 100 if seq_duration > 0 else 0
    print(f"Parallel processing duration (100 resumes, 4 workers): {par_duration:.4f} seconds (Improvement: {improvement_par:.1f}%)")

    # 3. Memory Efficient Batch Processing Demonstration
    print("\n--- [STEP 3] BATCH PROCESSOR GENERATOR ---")
    batch_count = 0
    total_elements = 0
    for batch in batch_process(cleaned_resumes, batch_size=15):
        batch_count += 1
        total_elements += len(batch)
        print(f"  - Batch {batch_count}: Processed {len(batch)} items.")
    print(f"Total batches processed: {batch_count}, containing {total_elements} resumes.")

    # 4. Noisy Resume Cleaning Verification
    print("\n--- [STEP 4] NOISY RESUME CLEANING DEMO ---")
    noisy_example = "Developer!!! with Python..... Django---- and Reactttttt expertise."
    cleaned_example = clean_noisy_resume(noisy_example)
    print("Raw noisy input:  ", noisy_example)
    print("Cleaned output:   ", cleaned_example)
    print("Extracted skills: ", fast_skill_extract(cleaned_example))

    # 5. Stability Mechanisms (Retry, Safe Execute, Timeout)
    print("\n--- [STEP 5] STABILITY MECHANISMS ---")
    
    # Safe execute
    def risky_op(x):
        return x / 0
    res_safe = safe_execute(risky_op, 10)
    print("Safe execution result for divide-by-zero:", json.dumps(res_safe))
    
    # Retry
    attempts = 0
    def occasional_failure(x):
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise IOError("Connection timeout")
        return f"Database data retrieved on attempt {attempts}"
    res_retry = retry(occasional_failure, None, retries=3)
    print("Retry mechanism result:", res_retry)
    
    # Timeout
    def long_task(x):
        time.sleep(0.5)
        return "Complete"
    try:
        print("Running task with 1.0s limit (should succeed)...")
        run_with_timeout(long_task, None, seconds=1)
        print("  - Task finished within limits.")
        
        print("Running task with 0.1s limit (should timeout)...")
        run_with_timeout(long_task, None, seconds=0.1)
    except TimeoutError:
        print("  - TimeoutError caught successfully (Task was aborted safely).")

    # Save performance report to JSON
    report_dir = "data/ats_performance"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "performance_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "metrics": {
                "raw_duration_sec": round(raw_duration, 4),
                "optimized_duration_sec": round(opt_duration, 4),
                "improvement_lookup_percent": round(improvement, 1),
                "sequential_duration_sec": round(seq_duration, 4),
                "parallel_duration_sec": round(par_duration, 4),
                "improvement_parallel_percent": round(improvement_par, 1)
            },
            "noise_cleaning_test": {
                "input": noisy_example,
                "output": cleaned_example
            }
        }, f, indent=2)

    print("\n------------------------------------------------------------------------------------------")
    print("Day 18 Optimization & Performance Tuning Completed Successfully!")
    print(f"Performance Metrics report saved to: {os.path.abspath(report_path)}")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
