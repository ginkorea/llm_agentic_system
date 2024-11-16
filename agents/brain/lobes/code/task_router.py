from typing import Optional
from agents.brain.lobes.module import Module
from agents.brain.prompts.structured.controller_prompt import ControllerPrompt
from agents.brain.core import Brain
from agents.brain.prompts.examples.code_examples import CodeExamples

# ManagerFunction: Task management and decision-making
class TaskRouter(Module):
    """Directs tasks to the appropriate module and manages workflow."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.4,
            memory_limit=3,
            system_message="You manage task routing and decision-making, sending tasks to other lobes, do not use this for actual tasks.",
        )
        self.examples = CodeExamples()

    def build_prompt_builder(self, brain: Optional['Brain'] = None, modules=None, tools=None, examples=None):
        """Builds a structured prompt builder for the module."""
        modules, tools, examples = self.parse_brain(brain)
        self.prompt_builder = ControllerPrompt(tools=tools, modules=modules,
                                                   examples=examples)
        print("Controller Prompt Builder Initialized for TaskRouter")