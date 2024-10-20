from agents.toolkit.bag import BagOfTools
from agents.brain.core import Brain

# Base Agent class
class Agent:
    def __init__(self, forget_threshold: int = 10, verbose: bool = True, memory_type: str = 'simple'):
        # Set the verbose flag
        self.verbose = verbose

        # Initialize available tools with descriptions
        self.toolkit = BagOfTools()
        self.toolkit.get_tools()

        # Initialize brain with toolkit
        self.brain = Brain(toolkit=self.toolkit, memory_type=memory_type, verbose=verbose, forget_threshold=forget_threshold)

    def process_input(self, user_input: str) -> str:
        """
        Process the input through the brain, which decides whether to use a tool or lobe.
        """
        return self.brain.process_input(user_input)

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
