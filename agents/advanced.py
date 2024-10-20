# agents/advanced.py

from agents.base import Agent


class AdvancedAgent(Agent):
    def __init__(self, memory_type: str = 'openvino'):
        super().__init__()  # Initialize base Agent attributes
        # Initialize memory with embeddings
        if memory_type == 'openvino':
            from agents.brain.memory.ov_embedded import OpenvinoMemoryWithEmbeddings
            memory = OpenvinoMemoryWithEmbeddings(forget_threshold=10)
        else:
            from agents.brain.memory.cuda_embedded import CudaMemoryWithEmbeddings
            memory = CudaMemoryWithEmbeddings(forget_threshold=10)
        # Initialize Brain with the toolkit and memory
        self.brain.memory = memory  # Set the memory

    def process_input(self, user_input: str) -> str:
        """
        Process the input by delegating to the brain's process_input method.
        """
        result = self.brain.process_input(user_input)
        return result

    def store_memory(self, user_input: str, response: str):
        """Store the user input and response in memory."""
        self.brain.store_memory(user_input, response)
