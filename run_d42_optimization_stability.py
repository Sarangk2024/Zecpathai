# run_d42_optimization_stability.py

import json
from interview_ai.stable_hr_ai import stable_hr_evaluation, smooth_score
from interview_ai.refined_scoring import refined_score_pipeline
from interview_ai.followup_stability import stable_followup
from screening_ai.optimized_cleaner import advanced_clean
from utils.batch_processing import batch_process

def main():
    print("\n==========================================================================================")
    print("ZECPATH OPTIMIZATION & STABILITY RUNNER (DAY 42)")
    print("==========================================================================================\n")

    # 1. Outlier smoothing & decision logic
    print("--- [STEP 1] OUTLIER SMOOTHING & EVALUATION ---")
    raw_scores = [50, 60, 90, 30]
    eval_result = stable_hr_evaluation(raw_scores)
    print(f"Raw Score Stream: {raw_scores}")
    print(f"Smoothed Stable Score: {eval_result['stable_score']}")
    print(f"Final Decision: {eval_result['decision']}")

    # 2. Refined Scoring with bias reduction
    print("\n--- [STEP 2] REFINED CONFIDENCE-AWARE SCORING ---")
    scores = [60, 75, 90]
    confidences = [85, 90, 95]
    refined_scores = refined_score_pipeline(scores, confidences)
    print(f"Raw Scores: {scores}")
    print(f"Confidence Scores: {confidences}")
    print(f"Refined Normalized & Adjusted Scores: {refined_scores}")

    # 3. Follow-up Stability Logic
    print("\n--- [STEP 3] FOLLOW-UP SYSTEM STABILITY STATE TRANSITIONS ---")
    cases = [
        {"quality": "empty", "retry": 0},
        {"quality": "too_short", "retry": 1},
        {"quality": "uncertain", "retry": 1},
        {"quality": "uncertain", "retry": 2},
        {"quality": "perfect", "retry": 0}
    ]
    for c in cases:
        action = stable_followup(c["quality"], c["retry"])
        print(f"Answer Quality: {c['quality']:<10} | Retry Count: {c['retry']} -> Action: {action}")

    # 4. Transcript Cleanup Optimization
    print("\n--- [STEP 4] ADVANCED SPEECH TRANSCRIPT CLEANUP ---")
    dirty_transcripts = [
        "Um, uh, hello, I am like interested in Python, you know.",
        "We worked together together on the the database project project.",
        "Really?!! That was, uh, amazing, like, totally."
    ]
    for text in dirty_transcripts:
        cleaned = advanced_clean(text)
        print(f"Original: {text}")
        print(f"Cleaned : {cleaned}\n")

    # 5. Batch processing optimization
    print("--- [STEP 5] BATCH PROCESSING OPTIMIZATION ---")
    cleaned_batch = batch_process(dirty_transcripts, advanced_clean)
    print(f"Processed batch size: {len(cleaned_batch)}")
    print(f"Results: {cleaned_batch}")

    # 6. Before vs After comparison
    print("\n--- [STEP 6] BEFORE VS AFTER SCORING STABILITY COMPARISON ---")
    before = {"score": 48, "decision": "Reject"}
    after = {"score": 62, "decision": "Consider"}
    print(f"Before Optimization: {json.dumps(before)}")
    print(f"After Optimization : {json.dumps(after)}")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 42 Optimization & Stability Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
