from typing import Tuple, List
from agents.toolkit import BagOfTools
from agents.brain import Brain


# Base Agent class
class Agent:
    def __init__(self):
        # Memory to store previous interactions
        self.brain = Brain()

        # Initialize available tools with descriptions
        self.toolkit = BagOfTools()
        self.toolkit.get_tools()
        self.verbose = True



    def store_memory(self, user_input: str, response: str):
        """Store the user input and response in memory."""
        self.brain.store_memory(user_input, response)

    def recall_memory(self, start: int, end: int, long_term: bool = False) -> List[dict]:
        """Return the memory (conversation history)."""
        if long_term:
            try:
                return self.brain.memory.long_term[start:end]
            except IndexError:
                return self.brain.memory.long_term
        try:
            return self.brain.memory.short_term[start:end]
        except IndexError:
            return self.brain.memory.short_term


    def determine_action(self, user_input: str, advanced: bool) -> (bool, int):
        """
        Determine whether to use a tool or LLM.
        If advanced is False, check if any tool matches the input.
        If advanced is True, it can be handled by the BrainAgent with the LLM.

        Returns:
            - (True, tool_index) if a tool should be used
            - (False, -1) if LLM should be used
        """
        if not advanced:
            return self.basic_determine_action(user_input)
        else:
            return self.advanced_determine_action(user_input)

    def basic_determine_action(self, user_input: str) -> (bool, int):
        """
        Determine whether to use a tool or LLM.
        If advanced is False, check if any tool matches the input.
        If advanced is True, it can be handled by the BrainAgent with the LLM.

        Returns:
            - (True, tool_index) if a tool should be used
            - (False, -1) if LLM should be used
        """
        b, idx = self.get_tool(user_input)
        if b: return b, idx
        return False, -1

    def advanced_determine_action(self, user_input: str) -> (bool, int, str, str):
        """
        Use the brain's frontal lobe (or other lobes) to determine if the input should
        be handled by a tool or an LLM. If a tool is chosen, return the index, the tool's name,
        and the refined prompt. If LLM is chosen, return -1, the lobe, and the prompt for the LLM.

        Returns:
            - (True, tool_index, tool_name, refined_prompt) if a tool should be used
            - (False, -1, lobe_name, refined_prompt) if LLM should be used
        """
        # Ask the frontal lobe to analyze the input and determine the best course of action
        decision = self.brain.determine_tool_or_llm(user_input)

        if decision['use_tool']:
            # The brain suggests using a tool, return the tool's details
            tool_index = self.get_tool(decision['tool_name'])[1]
            return True, tool_index, decision['tool_name'], decision['refined_prompt']

        # The brain suggests using an LLM
        return False, -1, decision['lobe'], decision['refined_prompt']

    def get_tool(self, user_input: str) -> Tuple[bool,int]:
        """
        Get the index of the tool with the given name.
        """
        # Use the basic logic to choose a tool or LLM
        for idx, _tool in enumerate(self.toolkit.tools):
            if _tool["name"] in user_input:
                return True, idx  # Return True and tool index
        return False, -1  # If no tool matched, use the LLM


    def use_tool(self, user_input: str, tool_index: int, sanitize: bool = False) -> str:
        """
        Use the tool at the given index with the appropriate user input.
        """
        chosen_tool = self.toolkit.tools[tool_index]["tool"]  # Access the tool function
        if sanitize:
            expression = user_input.replace(self.toolkit.tools[tool_index]["name"], "").strip()
        else:
            expression = user_input
        if self.verbose:
            print(f"Using tool '{self.toolkit.tools[tool_index]['name']}' with expression: '{expression}'")
        # Use invoke instead of __call__
        return chosen_tool.invoke(expression)  # Call the tool function with the expression



    def process_input(self, user_input: str, reasoning: bool = False, sanitize: bool = True) -> str:
        """
        Process the input by deciding whether to throw a tool or use a model.
        """
        # Determine action: tool (True) or LLM (False)
        use_tool, tool_index = self.determine_action(user_input, reasoning)

        if use_tool:
            # Use the identified tool
            return self.use_tool(user_input, tool_index, sanitize)

        # In the base class, we'll simply return a placeholder response
        return f"Base Agent: I don't know how to respond to '{user_input}'"

    def run(self):
        """Main method to interact with the agent."""
        print("Agent is now running. Type 'exit' to stop.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            # Process the input and get a response
            response = self.process_input(user_input)
            print(f"Agent: {response}")


# Example usage
if __name__ == "__main__":
    # Instantiate the base Agent
    agent = Agent()

    # Start interaction loop
    agent.run()
