from agents.brain.core import Brain
from agents.brain.lobes.code_lobes import (
    TaskRouter, LogicLobe, DebuggerLobe, SeniorDev, SyntaxLobe,
    DocumentationLobe, TestingLobe, OptimizerLobe, RefactorLobe, GoalSetter
)
from agents.brain.prompts.examples.code_examples import CodeExamples
from agents.brain.goal.software_dev_goal import SoftwareDevelopmentGoal

class CodeBrain(Brain):
    def __init__(self, toolkit, forget_threshold: int = 10, verbose: bool = True, memory_type='cuda', goal_file=None, goal=None):
        super().__init__(toolkit, forget_threshold, verbose, memory_type, goal_file=goal_file, goal=goal)

        self.tool_descriptions = self.build_tool_descriptions()

        # Add code-focused lobes to the brain
        self.modules = [
            TaskRouter(),      # Task manager directing to other lobes
            LogicLobe(),            # Responsible for structuring code logic
            DebuggerLobe(),         # Primary debugger for initial error resolution
            SeniorDev(),            # Advanced debugging for complex issues
            SyntaxLobe(),           # Generates syntax and boilerplate code
            DocumentationLobe(),    # Creates documentation and comments
            TestingLobe(),          # Generates tests to verify code functionality
            OptimizerLobe(),        # Optimizes code for efficiency and readability
            RefactorLobe(),          # Refactors code to improve clarity and best practices
            GoalSetter()            # Sets and manages software development goals
        ]

        # Pre-generate descriptions for tools and modules
        self.module_descriptions = self.build_module_descriptions(include_routing_module=False)
        self.examples = CodeExamples()
        self.router = self.modules[0]
        self.goal_setter = self.modules[-1]
        self.initialize_prompt_builders()

        # Set the goal and milestones for chaining mode
        self.goal = SoftwareDevelopmentGoal(None, None, goal_file=goal_file)
        self.goal.description = self.goal.set_unique_goal_from_file(brain=self)

        if self.verbose:
            print("CodeBrain initialized.")
            print("Goal set:", self.goal.description)
            for i, milestone in enumerate(self.goal.milestones):
                print(f"Milestone {i}: {milestone.description}")




