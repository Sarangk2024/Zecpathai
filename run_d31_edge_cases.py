# run_d31_edge_cases.py - Standalone edge case and failure handling runner (Day 31).

import json
from screening_ai.robust_flow import detect_edge_case, handle_edge_case
from screening_ai.error_framework import get_error_response, fallback_strategy
from screening_ai.noise_handler import clean_noise, detect_language_mix

def main():
    print("\n==========================================================================================")
    print("ZECPATH EDGE CASE & FAILURE HANDLING RUNNER (DAY 31)")
    print("==========================================================================================\n")

    # 1. Example executions of Edge Cases
    print("--- [STEP 1] TESTING EDGE CASE DETECTION ---")
    test_cases = [
        {"answer": "", "confidence": 1.0, "retry": 0},
        {"answer": "hello", "confidence": 0.4, "retry": 0},
        {"answer": "um yes", "confidence": 0.9, "retry": 1},
        {"answer": "enna chetta bhai", "confidence": 1.0, "retry": 0},
        {"answer": "Python", "confidence": 1.0, "retry": 0},
        {"answer": "I have 3 years of experience in Django", "confidence": 0.95, "retry": 0}
    ]

    for tc in test_cases:
        issue = detect_edge_case(tc["answer"], tc["confidence"])
        action = handle_edge_case(None, tc["answer"], tc["confidence"], tc["retry"])
        resp = get_error_response(issue)
        print(f"Answer:     \"{tc['answer']}\" (Confidence: {tc['confidence']})")
        print(f"Issue:      {issue}")
        print(f"Action:     {action}")
        print(f"Response:   \"{resp}\"")
        print("-" * 50)

    # 2. Cleanup demo
    print("\n--- [STEP 2] CLEANING BACKGROUND NOISE & DUPLICATIONS ---")
    dirty_text = "I like [cough] Javaaaaa and Django---- [background noise]"
    cleaned = clean_noise(dirty_text)
    print(f"Dirty Text:   \"{dirty_text}\"")
    print(f"Cleaned Text: \"{cleaned}\"")

    # 3. Fallback strategy demo
    print("\n--- [STEP 3] SAFETY FALLBACK RULES ---")
    print(f"Fallback ('missing', Retry count 0): {fallback_strategy('missing', 0)}")
    print(f"Fallback ('missing', Retry count 2): {fallback_strategy('missing', 2)}")
    print(f"Fallback ('language_mix', Retry count 0): {fallback_strategy('language_mix', 0)}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 31 Edge Case & Failure Handling Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
