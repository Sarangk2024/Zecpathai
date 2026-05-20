# run_d40_interview_simulation.py - Standalone HR interview simulation runner (Day 40).

import json
from tests.simulate_hr_interview import run_all_simulations

def main():
    print("\n==========================================================================================")
    print("ZECPATH HR INTERVIEW END-TO-END SIMULATION RUNNER (DAY 40)")
    print("==========================================================================================\n")

    # Execute all candidate simulations
    print("--- [STEP 1] EXECUTING MULTIPLE CANDIDATE INTERVIEW SIMULATIONS ---")
    results = run_all_simulations()
    
    for cid, report in results.items():
        print(f"\n==================================================")
        print(f"SIMULATED PROFILE: {cid}")
        print(f"==================================================")
        print(f"Overall Score:  {report['overall_score']}")
        print(f"Decision:       {report['decision']}")
        print(f"Cultural Fit:   {report['summary']['cultural_fit']}")
        print(f"Strengths:      {report['summary']['strengths']}")
        print(f"Weaknesses:     {report['summary']['weaknesses']}")
        print(f"Risks:          {report['summary']['risks']}")
        print(f"Inconsistencies:{report['summary']['inconsistencies']}")
        print("\nNatural Language Summary:")
        print(report["natural_language_summary"])
        print("-" * 50)

    print("\n------------------------------------------------------------------------------------------")
    print("Day 40 HR Interview Simulation Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
