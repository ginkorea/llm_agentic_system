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

    def build_prompt(self, prd_text: str, previous_output: bool = False, previous_module: Optional[str] = None, goal: Goal = None, **kwargs) -> str:
        """
        Builds the prompt to generate UML diagrams and architecture designs.

        Parameters:
        - prd_text: Text from the PRD.

        Returns:
        - A formatted prompt string.
        """
        self.prompt = f"""
        {self.base_prompt}
        
        Example PRD and Outputs:
        ----------------
        {self.examples}
        
        ----------------
        The examples above are for reference only. Your design should be based on the provided PRD.
        Ensure you provide as much detail as possible in your UML Diagram and Architecture Design, this will be more in depth than the examples provided and should be tailored to the PRD.

        PRD to Analyze (below):
        ----------------
        {prd_text}
        ----------------

        Generate the outputs as described above.  Ensure that prior to code block include the title of the output in markdown (i.e. # UML Diagram or # Architecture Design)
        """
        return self.prompt


