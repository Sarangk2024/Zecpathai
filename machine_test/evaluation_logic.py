# machine_test/evaluation_logic.py

# -------------------------------
# Correctness Evaluation
# -------------------------------
def correctness_score(passed, total):
    if total == 0:
        return 0
    return passed / total

# -------------------------------
# Efficiency Score (runtime)
# -------------------------------
def efficiency_score(runtime):
    if runtime < 1:
        return 1.0
    elif runtime < 2:
        return 0.7
    return 0.4

# -------------------------------
# Code Quality Score
# -------------------------------
def code_quality_score(code):
    length = len(code.splitlines()) if code else 0
    if length < 20:
        return 1.0
    elif length < 50:
        return 0.7
    return 0.4

# -------------------------------
# Problem-Solving Score
# -------------------------------
def problem_solving_score(attempts):
    if attempts == 1:
        return 1.0
    elif attempts <= 3:
        return 0.7
    return 0.4

# -------------------------------
# Final Task Score
# -------------------------------
def calculate_task_score(passed, total, runtime, code, attempts):
    correctness = correctness_score(passed, total)
    efficiency = efficiency_score(runtime)
    quality = code_quality_score(code)
    problem = problem_solving_score(attempts)
    
    final = (
        correctness * 0.4 +
        efficiency * 0.2 +
        quality * 0.2 +
        problem * 0.2
    )
    return {
        "task_score": round(final * 100, 2),
        "breakdown": {
            "correctness": round(correctness, 2),
            "efficiency": round(efficiency, 2),
            "code_quality": round(quality, 2),
            "problem_solving": round(problem, 2)
        }
    }

# -------------------------------
# Time-Based Scoring Logic
# -------------------------------
def time_score(time_taken, limit):
    ratio = time_taken / limit if limit > 0 else 1.0
    if ratio <= 0.5:
        return 1.0
    elif ratio <= 1.0:
        return 0.7
    return 0.4

# -------------------------------
# Machine Test Scoring Pipeline
# -------------------------------
def machine_test_pipeline(data):
    score = calculate_task_score(
        data["execution_results"]["passed"],
        data["execution_results"]["total"],
        data["execution_results"]["runtime"],
        data["code_snapshot"],
        data["attempts"]
    )
    time_factor = time_score(data["time_taken"], 30)
    final_score = (score["task_score"] * 0.8) + (time_factor * 100 * 0.2)
    return {
        "final_score": round(final_score, 2),
        "details": score
    }
