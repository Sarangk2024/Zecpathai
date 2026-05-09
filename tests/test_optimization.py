# tests/test_optimization.py - Optimization and Performance Unit Tests.

import pytest
import time
from ats_engine.optimized_engine import (
    clean_text_cached,
    fast_skill_extract,
    clean_noisy_resume,
    process_resumes_parallel,
    batch_process,
    safe_execute,
    retry,
    run_with_timeout
)

def test_clean_text_cached():
    text = "Python developer!!! with Django---- experience"
    # First call - parses and caches
    res1 = clean_text_cached(text)
    # Second call - retrieves from cache
    res2 = clean_text_cached(text)
    assert res1 == "python developer with django---- experience"
    assert res1 == res2

def test_fast_skill_extract():
    text = "I am a Python developer who loves React and django framework."
    skills = fast_skill_extract(text)
    assert "python" in skills
    assert "react" in skills
    assert "django" in skills
    assert "java" not in skills

def test_clean_noisy_resume():
    text = "Python developer!!! with Django---- experience...... and Javaaaaa code"
    cleaned = clean_noisy_resume(text)
    # Checks repeated character reduction (e.g., 'aaaa' to 'a', multiple '-' to none)
    assert "java" in cleaned
    assert "!!!" not in cleaned
    assert "----" not in cleaned

def test_batch_process():
    data = list(range(25))
    batches = list(batch_process(data, batch_size=10))
    assert len(batches) == 3
    assert len(batches[0]) == 10
    assert len(batches[2]) == 5

def test_parallel_processing():
    resumes = [
        "Python developer with Django experience",
        "React developer and Node expert",
        "Java backend developer with SQL knowledge"
    ]
    results = process_resumes_parallel(resumes, fast_skill_extract, max_workers=2)
    assert len(results) == 3
    assert "python" in results[0]
    assert "react" in results[1]
    assert "java" in results[2]

def test_safe_execute():
    def broken_func(data):
        raise ValueError("Something went wrong")
    
    res = safe_execute(broken_func, "some_data")
    assert "error" in res
    assert "Something went wrong" in res["error"]

def test_retry():
    call_count = 0
    def failing_func(data):
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise ValueError("Failure")
        return "Success"
        
    res = retry(failing_func, "some_data", retries=3)
    assert res == "Success"
    assert call_count == 2

def test_timeout_protection():
    def slow_func(data):
        time.sleep(0.5)
        return "Done"
        
    # Should complete since timeout is 2 seconds
    res = run_with_timeout(slow_func, "data", seconds=2)
    assert res == "Done"
    
    # Should timeout since sleep is 0.5 and limit is 0.1
    with pytest.raises(TimeoutError):
        run_with_timeout(slow_func, "data", seconds=0.1)
