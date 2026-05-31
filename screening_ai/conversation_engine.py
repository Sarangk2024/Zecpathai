# screening_ai/conversation_engine.py

class ConversationStateMachine:
    def __init__(self, flow):
        self.flow = flow["nodes"]
        self.current_node = flow["start"]
        self.retry_count = {}

    def get_question(self):
        return self.flow[self.current_node]["question"]

    def next(self):
        self.current_node = self.flow[self.current_node].get("next", "END")

    def handle_silence(self):
        node = self.flow[self.current_node]
        retry_node = node.get("on_silence")
        if retry_node:
            self.retry_count.setdefault(self.current_node, 0)
            self.retry_count[self.current_node] += 1
            if self.retry_count[self.current_node] <= node.get("max_retries", 2):
                self.current_node = retry_node
            else:
                self.current_node = "END"
        else:
            self.current_node = "END"

    def handle_confusion(self):
        node = self.flow[self.current_node]
        if "on_confusion" in node:
            self.current_node = node["on_confusion"]

    def handle_repeat(self):
        node = self.flow[self.current_node]
        if "on_repeat" in node:
            self.current_node = node["on_repeat"]

    def is_end(self):
        return self.current_node == "END"
