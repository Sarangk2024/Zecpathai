# ats_engine/optimized_engine.py - Performance tuning and optimization for Zecpath ATS.

import re
import time
import platform
import threading
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

# -------------------------------
# Cached Text Cleaning (Faster Reuse)
# -------------------------------
@lru_cache(maxsize=1000)
def clean_text_cached(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\.\,\-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------------
# Parallel Processing for Resumes
# -------------------------------
def process_resumes_parallel(resume_texts, process_function, max_workers=4):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_function, text) for text in resume_texts]
        for future in futures:
            results.append(future.result())
    return results

# -------------------------------
# Lightweight Skill Extraction (Optimized)
# -------------------------------
SKILLS = ["python", "java", "react", "node", "sql", "django"]

def fast_skill_extract(text):
    cleaned = clean_text_cached(text)
    # Match skills efficiently
    return [skill for skill in SKILLS if skill in cleaned]

# -------------------------------
# Memory Efficient Processing
# -------------------------------
def batch_process(data, batch_size=10):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

# -------------------------------
# Noisy Resume Handling
# -------------------------------
def clean_noisy_resume(text):
    cleaned = clean_text_cached(text)
    # Remove repeated characters (3 or more)
    cleaned = re.sub(r"(.)\1{2,}", r"\1", cleaned)
    # Remove excessive symbols
    cleaned = re.sub(r"[\.\,\-]{2,}", "", cleaned)
    # Strip any extra spaces created
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()

# -------------------------------
# Stability Improvements
# -------------------------------
def safe_execute(func, data):
    try:
        return func(data)
    except Exception as e:
        return {"error": str(e)}

def retry(func, data, retries=3, delay=0.1):
    for attempt in range(retries):
        try:
            return func(data)
        except Exception as e:
            if attempt == retries - 1:
                return {"error": f"Failed after {retries} retries: {str(e)}"}
            time.sleep(delay)
    return {"error": "Failed after retries"}

# -------------------------------
# Timeout Protection (Platform-Safe)
# -------------------------------
def timeout_handler(signum, frame):
    raise TimeoutError("Timeout limit exceeded")

def run_with_timeout(func, data, seconds=5):
    """
    Executes a function with a timeout limit.
    Uses signal.alarm on Unix platforms, and a thread join mechanism on Windows to prevent crashes.
    """
    if platform.system() != 'Windows':
        import signal
        # Register the signal handler
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(seconds)
        try:
            result = func(data)
            return result
        finally:
            # Disable the alarm
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    else:
        # Windows-safe thread-based timeout
        result_holder = {}
        exception_holder = {}
        
        def worker():
            try:
                result_holder['val'] = func(data)
            except Exception as ex:
                exception_holder['val'] = ex

        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
        thread.join(seconds)
        
        if thread.is_alive():
            raise TimeoutError("Timeout limit exceeded")
        if 'val' in exception_holder:
            raise exception_holder['val']
        return result_holder.get('val')
