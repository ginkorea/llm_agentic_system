# goal_builder_prompt.py

from typing import Optional
from agents.brain.prompts.structured import StructuredPrompt
from agents.brain.goal.goal import Goal

class GoalBuilderPrompt(StructuredPrompt):
    """
    Specialized prompt class for building a unique goal from a PRD or similar document.
    This prompt guides the agent in interpreting key requirements and constructing a goal statement.
    """

    def __init__(self, tools: Optional[str] = None, modules: Optional[str] = None,
                 examples: Optional[str] = None):
        super().__init__(tools, modules, examples)
        self.base_prompt = f"""
        You are the Goal Builder module, responsible for interpreting requirements documents to create a clear and actionable end goal.
        Your task is to extract the primary objective from the following document and construct a concise goal statement.

        Please respond with the extracted goal description in a clear and concise manner, this will be the overall goal for the project.

        """
        self.reset_prompt()  # Initialize prompt to GoalBuilder's base prompt

    def build_prompt(self, prd_text: str, previous_output: bool = False, previous_module: Optional[str] = None, goal: Goal = None) -> str:
        """
        Constructs the prompt based on the provided PRD or requirements document text.

        Parameters:
        - prd_text: The text of the PRD or requirements document.

        Returns:
        - A formatted prompt string ready for the LLM to interpret and generate a goal description.
        """
        self.reset_prompt()  # Reset to the base prompt

        # Build prompt specifically for goal extraction
        self.prompt += f"""
        Document to interpret:
        ----------------
        {prd_text}
        ----------------

        Based on the content above, create a goal statement that captures the primary objective.  RESPOND IN LESS THAN 3 SENTENCES.
        
        example_1: "Develop a mobile app that allows users to track their daily exercise and nutrition with the following features: ..."
        example_2: "Create a web-based platform for managing customer data and generating reports based on user input that ..."
        
        """
        print("self.prompt for GoalBuilder:", self.prompt)
        return self.prompt
