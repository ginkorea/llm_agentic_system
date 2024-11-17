from agents.toolkit.bag import BagOfTools

# Base Agent class
class Agent:
    def __init__(self, forget_threshold=10, verbose=True, memory_type='simple', brain_type='simple', chaining=False, goal=None, goal_file=None):
        self.verbose = verbose
        self.toolkit = BagOfTools()
        self.toolkit.get_tools()
        self.chaining = chaining
        if brain_type == 'simple':
            from agents.brain.core import Brain
            self.brain = Brain(toolkit=self.toolkit, forget_threshold=forget_threshold, verbose=verbose, memory_type=memory_type, goal=goal, goal_file=goal_file)
        elif brain_type == 'code':
            from agents.brain.code_brain_model import CodeBrain
            self.brain = CodeBrain(toolkit=self.toolkit, forget_threshold=forget_threshold, verbose=verbose, memory_type=memory_type, goal=goal, goal_file=goal_file)
        elif brain_type == 'cognitive':
            from agents.brain.cognitive import CognitiveBrain
            self.brain = CognitiveBrain(toolkit=self.toolkit, forget_threshold=forget_threshold, verbose=verbose, memory_type=memory_type, goal=goal, goal_file=goal_file)

    def store_memory(self, user_input: str, response: str, module: str):
        """Store the user input and response in memory."""
        self.brain.memory.store(user_input, response, module)

    def run(self):
        if self.chaining:
            current_input = self.brain.goal.get_progress_description()
            while not self.brain.goal.is_complete():
                results, judge_output, achieved, using = self.brain.process_input(current_input, chaining_mode=True)
                current_input = self.concat_results(results, judge_output, achieved, using)
                if self.verbose:
                    print(current_input)
        else:
            while True:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    break
                response, _, _, _ = self.brain.process_input(user_input)
                print("Agent:", response)

    @staticmethod
    def concat_results(original_results, judge_results, achieved, using):
        """Concatenate the results from the original input and the judge output."""
        results = f"Original Results:\n{original_results}\nusing {using}\nGoal Achieved: {achieved} \nJudge Results:\n{judge_results}"
        return results


    def goal_achieved(self):
        """Check if the overall goal has been achieved by updating and checking milestones."""
        return self.brain.goal.update_progress()


# Example usage
if __name__ == "__main__":
    # Instantiate the base Agent
    agent = Agent(brain_type='code')
    agent.brain.initialize_prompt_builders()  # Initialize prompt builders for all modules

    # Start interaction loop
    agent.run()
