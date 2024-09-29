from langchain_openai import ChatOpenAI
from .lobes import PreFrontalCortex, OccipitalLobe, FrontalLobe, TemporalLobe, ParietalLobe, Cerebellum, Hippocampus, \
    BrocasArea, Amygdala, CerebralCortex
from .memory import Memory


class Brain:
    def __init__(self, forget_threshold: int = 10):
        self.memory = Memory(forget_threshold=forget_threshold)

        # Initialize lobes using the specialized classes
        self.lobes = [
            PreFrontalCortex(),
            FrontalLobe(),
            OccipitalLobe(),
            TemporalLobe()  # Add other lobes as needed
        ]

    def get_lobe_info(self):
        """
        Dynamically generates a list of available lobes and their descriptions.
        """
        lobe_info = {}
        for idx, lobe in enumerate(self.lobes):
            lobe_info[idx] = lobe.get_info()
        return lobe_info

    def determine_lobe(self, user_input: str, reasoning: bool) -> dict:
        """
        Dynamically determine which lobe should handle the task by passing the decision-making to the PreFrontalCortex.
        The response should provide the lobe index and the updated input for that lobe to process.
        """
        # Dynamically fetch the lobe options
        lobe_options = self.get_lobe_info()

        prompt = {
            "lobes": lobe_options,
            "task_description": user_input
        }

        # The prefrontal cortex determines which lobe should handle the input
        decision_response = self.lobes[0].process(user_input=str(prompt), memory=self.memory.short_term)

        # Assuming decision_response contains the index of the lobe to use and the prompt to evaluate
        decision = eval(decision_response)  # Be cautious with eval in real scenarios; here we assume trusted input
        lobe_index = decision.get('lobe', 0)  # Default to PreFrontalCortex
        new_prompt = decision.get('prompt', user_input)

        return {"lobe_index": lobe_index, "prompt": new_prompt}

    def process_input(self, user_input: str, reasoning: bool = False) -> str:
        """
        Process input using the appropriate lobe and send the brain's memory to the lobe.
        """
        lobe_info = self.determine_lobe(user_input, reasoning)
        selected_lobe = self.lobes[lobe_info["lobe_index"]]

        # Pass memory to the selected lobe and get the response
        return selected_lobe.process(user_input=lobe_info["prompt"], memory=self.memory.short_term)

    def store_memory(self, user_input: str, response: str):
        """Store the user input and response in memory."""
        # Add prompt-response pair to memory




