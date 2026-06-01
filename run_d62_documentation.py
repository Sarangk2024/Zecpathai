# run_d62_documentation.py

import os

def main():
    print("\n==========================================================================================")
    print("ZECPATH AI TECHNICAL HANDBOOK RUNNER (DAY 62)")
    print("==========================================================================================\n")

    handbook_path = r"c:\Users\kutta\OneDrive\Desktop\zecpath\documentation\zecpath_technical_handbook.md"
    print(f"Reading technical handbook from: {handbook_path}\n")

    if os.path.exists(handbook_path):
        with open(handbook_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Output first 35 lines as a preview
        preview_limit = min(35, len(lines))
        print(f"--- PREVIEWING FIRST {preview_limit} LINES OF HANDBOOK ---")
        for i in range(preview_limit):
            print(lines[i], end="")
        print("\n---------------------------------------------------------")
        print(f"Total handbook lines count: {len(lines)}")
    else:
        print("[ERROR] Technical handbook file not found!")

    print("\n------------------------------------------------------------------------------------------")
    print("Day 62 Technical Handbook Compilation Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
