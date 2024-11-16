# software_design_prompt.py

from agents.brain.prompts.structured.structured_prompt import StructuredPrompt
from agents.brain.goal.goal import Goal
from typing import Optional

class SoftwareDesignPrompt(StructuredPrompt):
    """
    Specialized prompt class for generating UML diagrams and architecture designs from PRD input.
    """

    def __init__(self, examples=None):
        super().__init__(examples=examples)
        self.base_prompt = """
        You are a software design expert. Your task is to analyze the provided PRD and generate:
        - A UML Diagram (properly formatted as a code block)
        - An Architecture Design (properly formatted as a code block)

        The output should be two distinct code blocks:
        - The first for the UML Diagram
        - The second for the Architecture Design

        Do not include any additional text. Just return the two code blocks.
        """

    def build_prompt(self, prd_text: str, previous_output: bool = False, previous_module: Optional[str] = None, goal: Goal = None) -> str:
        """
        Builds the prompt to generate UML diagrams and architecture designs.

        Parameters:
        - prd_text: Text from the PRD.

        Returns:
        - A formatted prompt string.
        """
        return f"""
        {self.base_prompt}
        
        Example PRD and Outputs:
        ----------------
        {self.examples}
        
        ----------------

        PRD to Analyze:
        ----------------
        {prd_text}
        ----------------

        Generate the outputs as described above.
        """
