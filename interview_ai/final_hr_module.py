# interview_ai/final_hr_module.py

from interview_ai.hr_scoring_engine import hr_scoring_pipeline
from ai_core.unified_scoring_engine import calculate_unified_score
from interview_ai.summary_generator import generate_interview_summary

def run_hr_interview(candidate_id, answers, communication, behavior):
    hr_result = hr_scoring_pipeline(answers)
    final_score = calculate_unified_score(
        ats_score=70,
        screening_score=75,
        hr_score=hr_result["hr_score"],
        weights={"ats": 0.3, "screening": 0.3, "hr": 0.4}
    )
    summary = generate_interview_summary(
        candidate_id,
        hr_result["details"],
        communication,
        behavior,
        answers
    )
    return {
        "candidate_id": candidate_id,
        "final_score": final_score,
        "decision": summary["decision"],
        "summary": summary
    }
