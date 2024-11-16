from agents.brain.lobes.module import Module
from agents.brain.prompts.examples.code_examples import CodeExamples
from agents.brain.prompts.structured.get_goal_from_file_prompt import GoalBuilderPrompt
from agents.brain.core import Brain
from typing import Optional

class GoalSetter(Module):
    """Sets the goal and milestones for the brain."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.4,
            memory_limit=3,
            system_message="You set the goal and milestones for the brain.",
        )
        self.examples = CodeExamples()

    @staticmethod
    def load_goal_examples(file_path: str) -> str:
        """Reads goal examples from a file."""
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Goal file '{file_path}' not found.")
            return "No examples provided."

    def build_prompt_builder(self, brain: Optional['Brain'] = None, modules=None, tools=None, examples=None):
        """Builds a structured prompt builder for the module."""
        modules, tools, _ = self.parse_brain(brain)
        print("GoalSetter modules:", modules)
        print("GoalSetter tools:", tools)
        print("GoalSetter examples:", _)
        print("GoalSetter goal file:", brain.goal_file)
        examples = self.load_goal_examples(brain.goal_file)
        self.prompt_builder = GoalBuilderPrompt(examples=examples)
        print("Goal Setter Prompt Builder Initialized for GoalSetter")