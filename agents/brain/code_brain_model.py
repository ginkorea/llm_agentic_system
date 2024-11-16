from agents.brain.core import Brain
from agents.brain.lobes.code import TaskRouter, GoalSetter, SoftwareDesigner, EnvironmentSetupManager
from agents.brain.prompts.examples import CodeExamples
from agents.brain.goal.software_dev_goal import SoftwareDevelopmentGoal

class CodeBrain(Brain):
    def __init__(self, toolkit, forget_threshold: int = 10, verbose: bool = True, memory_type='cuda', goal_file=None, goal=None):
        super().__init__(toolkit, forget_threshold, verbose, memory_type, goal_file=goal_file, goal=goal)

        self.tool_descriptions = self.build_tool_descriptions()

        # Add code-focused lobes to the brain
        self.modules = [
            TaskRouter(),               # Task manager directing to other lobes
            SoftwareDesigner(),         # Designs software architecture and logic
            EnvironmentSetupManager(),  # Sets up the development environment
            GoalSetter()                # Sets and manages software development goals
        ]

        # Pre-generate descriptions for tools and modules
        self.module_descriptions = self.build_module_descriptions(include_routing_module=False)
        self.examples = CodeExamples()
        self.router = self.modules[0]
        self.goal_setter = self.modules[-1]
        self.initialize_prompt_builders()

        # Load PRD content from file
        self.knowledge_base.update(self.load_prd_from_file())

        # Set the goal and milestones for chaining mode
        self.goal = SoftwareDevelopmentGoal(None, None, goal_file=goal_file)
        self.goal.description = self.goal.set_unique_goal_from_file(brain=self)


        if self.verbose:
            print("CodeBrain initialized.")
            print("PRD: ", self.knowledge_base["prd"] if "prd" in self.knowledge_base else "No PRD loaded.")
            print("Goal set:", self.goal.description)
            for i, milestone in enumerate(self.goal.milestones):
                print(f"Milestone {i}: {milestone.description}")


    def load_prd_from_file(self) -> dict[str, str]:
        """
        Reads the PRD content from the specified file.

        Parameters:
        - None

        Returns:
        - dict: A dictionary containing the PRD content with the key 'prd'.
        """
        key = "prd"
        try:
            with open(self.goal_file, "r") as prd_file:
                return {key: prd_file.read()}
        except FileNotFoundError:
            print(f"Error: The file '{self.goal_file}' was not found.")
            return {key: ""}
        except Exception as e:
            print(f"Error reading the file '{self.goal_file}': {e}")
            return {key: ""}





