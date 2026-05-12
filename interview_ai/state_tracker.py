# interview_ai/state_tracker.py

class InterviewState:
    def __init__(self):
        self.history = []
        self.asked_questions = set()
        
    def add_interaction(self, question, answer):
        self.history.append({
            "question": question,
            "answer": answer
        })
        self.asked_questions.add(question)
        
    def is_repeated(self, question):
        return question in self.asked_questions

def avoid_repetition(state, question_pool):
    return [q for q in question_pool if not state.is_repeated(q)]
