# tests/simulate_hr_interview.py

from interview_ai.question_generator import generate_questions
from interview_ai.communication_engine import calculate_communication_score
from interview_ai.behavior_analyzer import analyze_behavior
from interview_ai.hr_scoring_engine import hr_scoring_pipeline
from interview_ai.summary_generator import generate_interview_summary

def run_candidate_simulation(candidate_id, role_type, exp_level, responses, durations):
    # Step 1: Generate questions (we can map responses to mock questions)
    questions = generate_questions(role_type, exp_level)
    
    # Step 2: Evaluate communications and behavior per question
    comm_scores = []
    behavior_reports = []
    
    # We will score each answer
    for idx, ans in enumerate(responses):
        dur = durations[idx] if idx < len(durations) else 5
        comm = calculate_communication_score(ans)
        beh = analyze_behavior(ans, dur)
        comm_scores.append(comm)
        behavior_reports.append(beh)
        
    # Step 3: Run through HR scoring pipeline
    # We need to construct answers objects for the scoring pipeline
    pipeline_answers = []
    for idx, ans in enumerate(responses):
        q_id = f"Q{idx+1}"
        comm = comm_scores[idx]
        beh = behavior_reports[idx]
        
        pipeline_answers.append({
            "question_id": q_id,
            "relevance_score": 0.9 if len(ans.split()) > 5 else 0.6,
            "communication_score": comm["communication_score"],
            "confidence_score": beh["confidence"]["confidence_score"],
            "contradiction": beh["contradiction"],
            "is_vague": beh["confidence"]["signals"]["uncertainty"] < 0.5
        })
        
    hr_result = hr_scoring_pipeline(pipeline_answers, exp_level)
    
    # Step 4: Aggregate into final summary
    # For overall aggregate summary: average communication and behavior
    avg_comm = sum(c["communication_score"] for c in comm_scores) / len(comm_scores)
    avg_beh = sum(b["behavioral_score"] for b in behavior_reports) / len(behavior_reports)
    avg_conf = sum(b["confidence"]["confidence_score"] for b in behavior_reports) / len(behavior_reports)
    
    overall_comm = {"communication_score": avg_comm}
    overall_beh = {
        "confidence": {"confidence_score": avg_conf},
        "contradiction": any(b["contradiction"] for b in behavior_reports),
        "behavioral_score": avg_beh
    }
    
    summary = generate_interview_summary(
        candidate_id=candidate_id,
        hr_scores=hr_result["details"],
        communication=overall_comm,
        behavior=overall_beh,
        answers=responses
    )
    
    return summary

def run_all_simulations():
    # Define candidate profiles
    profiles = {
        "C_CONFIDENT": {
            "role": "technical",
            "exp": "experienced",
            "answers": [
                "I am a software engineer with strong experience because I built several backend APIs.",
                "First I analyze the problem, then prioritize core features, and finally execute the plan.",
                "I communicate regularly and resolve conflicts by trying to understand all teammate views."
            ],
            "durations": [6, 7, 8]
        },
        "C_HESITANT": {
            "role": "non_technical",
            "exp": "fresher",
            "answers": [
                "um uh i think i worked in teams maybe.",
                "i don't know sorry, but I guess I will try my best.",
                "um uh maybe 3 years but I'm not sure really."
            ],
            "durations": [12, 10, 15]
        }
    }
    
    results = {}
    for cid, data in profiles.items():
        results[cid] = run_candidate_simulation(
            candidate_id=cid,
            role_type=data["role"],
            exp_level=data["exp"],
            responses=data["answers"],
            durations=data["durations"]
        )
    return results

if __name__ == "__main__":
    res = run_all_simulations()
    print(res)
