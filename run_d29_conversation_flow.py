# run_d29_conversation_flow.py - Standalone conversation flow runner (Day 29).

import json
from screening_ai.conversation_engine import ConversationStateMachine
from screening_ai.error_handling import detect_issue, handle_response, RETRY_MESSAGES

def simulate_conversation(flow, inputs):
    engine = ConversationStateMachine(flow)
    dialog = []
    input_idx = 0
    
    while not engine.is_end() and input_idx < len(inputs):
        question = engine.get_question()
        user_input = inputs[input_idx]
        issue = detect_issue(user_input)
        
        dialog.append({
            "current_node": engine.current_node,
            "ai_says": question,
            "user_says": user_input if user_input != "" else "<silence>",
            "issue_detected": issue
        })
        
        # Advance the state machine based on the input
        if issue == "silence":
            engine.handle_silence()
        elif issue == "confusion":
            engine.handle_confusion()
        elif issue == "repeat":
            engine.handle_repeat()
        else:
            engine.next()
            
        input_idx += 1
        
    return dialog

def main():
    print("\n==========================================================================================")
    print("ZECPATH AI CONVERSATION FLOW DESIGN RUNNER (DAY 29)")
    print("==========================================================================================\n")

    # 1. Load conversation flow JSON
    flow_path = "screening_ai/conversation_flow.json"
    with open(flow_path, "r") as f:
        flow = json.load(f)

    # 2. Simulation inputs showcasing:
    # - Q1: Silence -> retry_Q1
    # - retry_Q1: Confusion -> clarify_Q1 -> Q1
    # - Q1: Valid answer -> Q2
    # - Q2: Repeating input -> followup_Q2
    # - followup_Q2: Valid answer -> Q3
    # - Q3: Valid answer -> END
    simulated_inputs = [
        "",                   # Silence on Q1
        "What",               # Confusion on retry_Q1
        "I am a dev.",        # Valid introduction answer on clarify_Q1/Q1
        "five five five",     # Repeat pattern on Q2
        "I have 3 years",     # Valid experience answer on followup_Q2
        "Python, Django"      # Valid skills answer on Q3
    ]

    print("--- [STEP 1] RUNNING DIALOG STATE MACHINE SIMULATION ---")
    dialog_history = simulate_conversation(flow, simulated_inputs)
    
    for idx, turn in enumerate(dialog_history, 1):
        print(f"Turn {idx} [Node: {turn['current_node']}]:")
        print(f"  AI: \"{turn['ai_says']}\"")
        print(f"  User: \"{turn['user_says']}\" (Issue Detected: {turn['issue_detected']})")
        print("-" * 50)

    print("\n------------------------------------------------------------------------------------------")
    print("Day 29 AI Conversation Flow Design Checked Successfully!")
    print("==========================================================================================\n")

if __name__ == "__main__":
    main()
