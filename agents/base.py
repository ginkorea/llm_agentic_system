from agents.toolkit.bag import BagOfTools

# Base Agent class
class Agent:
    def __init__(self, forget_threshold: int = 10, verbose: bool = True, memory_type: str = 'simple', brain_type: str = 'simple', chaining: bool = False, goal: str = None, milestones: list = None):
        # Set the verbose flag
        self.verbose = verbose

        # Initialize available tools with descriptions
        self.toolkit = BagOfTools()
        self.toolkit.get_tools()

        self.chaining = chaining

        # Set the goal and milestones for chaining mode
        if chaining:
            self.goal = goal
            self.milestone = milestones
        else:
            self.goal = None
            self.milestone = None

        # Initialize brain with toolkit
        if brain_type == 'simple':
            from agents.brain.core import Brain
            self.brain = Brain(toolkit=self.toolkit, forget_threshold=forget_threshold, verbose=verbose, memory_type=memory_type)
        elif brain_type == 'cognitive':
            from agents.brain.cognitive import CognitiveBrain
            self.brain = CognitiveBrain(toolkit=self.toolkit, forget_threshold=forget_threshold, verbose=verbose, memory_type=memory_type)
        elif brain_type == 'code':
            from agents.brain.code_brain_model import CodeBrain
            self.brain = CodeBrain(toolkit=self.toolkit, forget_threshold=forget_threshold, verbose=verbose, memory_type=memory_type)

    def process_input(self, user_input: str) -> str:
        """
        Process the input through the brain, which decides whether to use a tool or lobe.
        """
        return self.brain.process_input(user_input)

    def store_memory(self, user_input: str, response: str, module: str):
        """Store the user input and response in memory."""
        self.brain.memory.store(user_input, response, module)

    def run(self):
        if self.chaining:
            # Start with the initial goal as the first input
            current_input = self.goal

            while not self.goal_achieved():
                # Process the current input through the brain
                result, using = self.process_input(current_input)

                # Output the result for debugging
                print(f"Output from {using}:", result)

                # Save to memory and update the current input with the last output
                current_input = result  # Use the result as the new input for the next iteration

        else:
            # Interactive mode code here
            while True:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    break
                response = self.brain.process_input(user_input)
                print("Agent:", response)


    def goal_achieved(self):
        """Determine if the goal has been achieved by checking milestones or criteria."""
        # Define logic to check if goal criteria or milestones have been met
        return False  # Placeholder

# Example usage
if __name__ == "__main__":
    # Instantiate the base Agent
    agent = Agent(brain_type='code')
    agent.brain.initialize_prompt_builders()  # Initialize prompt builders for all modules

    # Start interaction loop
    agent.run()
