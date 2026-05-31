# interview_ai/aptitude_pipeline.py

from interview_ai.aptitude_scoring import calculate_aptitude_score
from interview_ai.scenario_evaluator import evaluate_scenario

def aptitude_pipeline(answer, scenario_type=None):
    score = calculate_aptitude_score(answer)
    scenario_score = None
    final_score = score["aptitude_score"]
    
    if scenario_type:
        scenario_score = evaluate_scenario(answer, scenario_type)
        final_score = (final_score * 0.7) + (scenario_score * 100 * 0.3)
        
    return {
        "aptitude_score": round(final_score, 2),
        "details": score,
        "scenario_score": scenario_score
    }
