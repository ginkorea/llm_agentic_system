# structured_prompt.py

from agents.brain.goal.goal import Goal
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from agents.brain.core import Brain  # Import only for type checking


class StructuredPrompt:
    """
    Base class for creating structured prompts for different brain modules (lobes).
    Initializes with optional tool descriptions, module descriptions, and examples.
    Allows flexible prompt construction, with support for building on previous output.
    """

    def __init__(self, tools: Optional[str] = None, modules: Optional[str] = None,
                 examples: Optional[str] = None, goal: Optional[Goal] = None):
        self.tools = tools or "No tools available."
        self.modules = modules or "No modules available."
        self.examples = examples or "No examples provided."
        self.base_prompt = "You are a brain module, responsible for handling specific task as part of a larger system. Respond to the following prompt based on the input."
        self.goal = goal # Goal object for tracking progress
        self.prompt = self.base_prompt # Initialize prompt to base prompt

    def build_prompt(self, brain: 'Brain', prompt_input: str, previous_output: bool = False,
                     previous_module: Optional[str] = None, goal: Goal = None) -> str:
        """
        Constructs the prompt based on user input, tools, modules, and examples.
        """
        self.reset_prompt(goal=goal)  # Start with a fresh prompt

        if previous_output:
            self.prompt += f"""
            React to the following output from the {previous_module} module:
            ----------------
            {prompt_input}
            ----------------
            """
        else:
            self.prompt += f"""
            React to the following input (it likely contains output from a previous LLM so it needs to be interpreted as such): "{prompt_input}"
            """
        return self.prompt

    def reset_prompt(self, goal=None) -> None:
        """
        Resets the prompt to the base prompt.
        """
        if goal:
            self.prompt = goal.get_progress_description() + goal.current_milestone().description + self.base_prompt
        else:
            self.prompt = self.base_prompt

    def set_goal(self, goal: Goal) -> None:
        """
        Sets the goal object for tracking progress.
        """
        self.goal = goal





