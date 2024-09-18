from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class Memory:

    def __init__(self, forget_threshold : int = 10, short_term=None, long_term=None):
        if long_term is None:
            self.long_term = []
        else: self.long_term = long_term
        if short_term is None:
            self.short_term = []
        else: self.short_term = short_term
        self.forget_threshold = forget_threshold
        self.visited_sites = []

class Brain:

    def __init__(self):
        self.memory = Memory()
        self.lobes = []
        # Initialize different lobes (models) for different tasks
        self.occipital_lobe = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)  # Simple tasks
        self.lobes.append(self.occipital_lobe)

    def store_memory(self, user_input: str, response: str):
        """Store the user input and response in memory."""
        self.memory.long_term.append({"user_input": user_input, "response": response})  # Store in long-term memory
        self.memory.short_term.append({"user_input": user_input, "response": response})
        if len(self.memory.short_term) > self.memory.forget_threshold:
            self.memory.short_term.pop(0)


class AdvancedBrain(Brain):

    def __init__(self, forget_threshold: int = 25):
        super().__init__()
        self.frontal_lobe = ChatOpenAI(model="gpt-4.0o", temperature=0.7)
        self.lobes.append(self.frontal_lobe)
        self.forgot_threshold = forget_threshold



