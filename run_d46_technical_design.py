# run_d46_technical_design.py

import json
from technical_ai.experience_logic import get_experience_level
from technical_ai.difficulty_engine import adjust_difficulty
from technical_ai.question_generator import generate_question

def main():
    print("\n==========================================================================================")
    print("ZECPATH TECHNICAL INTERVIEW AI DESIGN RUNNER (DAY 46)")
    print("==========================================================================================\n")

    # 1. Experience segmentation
    print("--- [STEP 1] EXPERIENCE-BASED SEGMENTATION ---")
    years_list = [1, 3, 7]
    for y in years_list:
        lvl = get_experience_level(y)
        print(f"Candidate Experience: {y} yrs -> Target Level: {lvl}")

    # 2. Difficulty adjustments
    print("\n--- [STEP 2] DYNAMIC DIFFICULTY PROGRESSION ---")
    states = [
        {"current": "basic", "quality": "good"},
        {"current": "intermediate", "quality": "good"},
        {"current": "advanced", "quality": "poor"},
        {"current": "intermediate", "quality": "poor"}
    ]
    for s in states:
        next_lvl = adjust_difficulty(s["current"], s["quality"])
        print(f"Current Difficulty: {s['current']:<12} | Answer Quality: {s['quality']:<4} -> Next Difficulty: {next_lvl}")

    # 3. Dynamic Question generation
    print("\n--- [STEP 3] DYNAMIC SKILL-BASED QUESTION GENERATION ---")
    skills = ["JavaScript", "Python"]
    diffs = ["basic", "intermediate", "advanced"]
    for s in skills:
        for d in diffs:
            q = generate_question(s, d)
            print(f"Skill: {s:<10} | Difficulty: {d:<12} -> Question: {q}")

    # 4. Interview State Structure printout
    print("\n--- [STEP 4] INTERVIEW STATE TRACKING STRUCTURE ---")
    state = {
        "candidate_id": "C2001",
        "role": "mern_developer",
        "experience_level": "3-5",
        "current_difficulty": "intermediate",
        "questions_asked": [
            {"skill": "JavaScript", "difficulty": "intermediate", "question": "Explain closures"}
        ],
        "scores": [85],
        "status": "in_progress"
    }
    print(json.dumps(state, indent=2))

    # 5. Diagram
    print("\n--- [STEP 5] INTERVIEW FLOW PROGRESSION DIAGRAM ---")
    diagram = """
    START
      |
    Introduction (Candidate background)
      |
    Experience Detection
      |
    Set Initial Difficulty
      |
    Ask Conceptual Questions
      |
    Evaluate Answer
      |
    Adjust Difficulty
      |
    Ask Problem-Solving Questions
      |
    Scenario-Based Questions
      |
    Advanced/System Design (if applicable)
      |
    Final Evaluation
      |
    Generate Technical Report
      |
    END
    """
    print(diagram)

    print("------------------------------------------------------------------------------------------")
    print("Day 46 Technical Interview System Design Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
