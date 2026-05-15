# tests/test_conversation.py

from screening_ai.conversation_engine import ConversationStateMachine
from screening_ai.error_handling import detect_issue, handle_response

def test_flow():
    flow = {
        "start": "Q1",
        "nodes": {
            "Q1": {"question": "Test", "next": "END"}
        }
    }
    engine = ConversationStateMachine(flow)
    assert engine.get_question() == "Test"

def test_detect_issue():
    assert detect_issue("      ") == "silence"
    assert detect_issue("what") == "confusion"
    assert detect_issue("python django python django python django") == "repeat"
    assert detect_issue("I have 3 years experience in python") == "valid"

def test_state_machine_transitions():
    flow = {
        "start": "Q1",
        "nodes": {
            "Q1": {
                "question": "Can you introduce yourself?",
                "next": "Q2",
                "on_silence": "retry_Q1"
            },
            "retry_Q1": {
                "question": "Sorry, could you introduce yourself?",
                "next": "Q2",
                "max_retries": 2
            },
            "Q2": {
                "question": "How many years of experience?",
                "next": "END"
            }
        }
    }
    engine = ConversationStateMachine(flow)
    assert engine.get_question() == "Can you introduce yourself?"
    
    # Simulate valid answer
    handle_response(engine, "I am a dev")
    assert engine.get_question() == "How many years of experience?"
    
    # Restart
    engine = ConversationStateMachine(flow)
    # Simulate silence
    handle_response(engine, "")
    assert engine.get_question() == "Sorry, could you introduce yourself?"
