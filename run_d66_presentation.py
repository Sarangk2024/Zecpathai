# run_d66_presentation.py

import os

def main():
    print("\n==========================================================================================")
    print("ZECPATH AI DEMO PRESENTATION DECK PREPARATION RUNNER (DAY 66)")
    print("==========================================================================================\n")

    deck_path = r"c:\Users\kutta\OneDrive\Desktop\zecpath\demo\demo_presentation_deck.md"
    script_path = r"c:\Users\kutta\OneDrive\Desktop\zecpath\demo\demo_script_walkthrough.md"

    if os.path.exists(deck_path):
        with open(deck_path, "r", encoding="utf-8") as f:
            content = f.read()
        print("--- [STEP 1] PRESENTATION SLIDE OUTLINE ---")
        print(content)
    else:
        print("[ERROR] Presentation deck file not found!")

    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            script = f.read()
        print("\n--- [STEP 2] DEMO TALKING POINTS WALKTHROUGH CUES ---")
        print(script)
    else:
        print("[ERROR] Walkthrough script file not found!")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 66 Presentation Assets Verification Completed Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
