# software_design_prompt.py

from agents.brain.prompts.structured.structured_prompt import StructuredPrompt
from agents.brain.goal.goal import Goal
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from agents.brain.core import Brain

class SoftwareDesignPrompt(StructuredPrompt):
    """
    Specialized prompt class for generating UML diagrams and architecture designs from PRD input.
    """

    def __init__(self, examples=None):
        super().__init__(examples=examples)
        self.base_prompt = """
        You are a software design expert. Your task is to analyze the provided PRD and generate:
        - A UML Class Diagram (properly formatted as a code block)
        - A UML Sequence Diagram (properly formatted as a code block)
        - An Architecture Design (properly formatted as a code block)

        The output should be three distinct code blocks:
        - The first for the UML Class Diagram
        - The second for the UML Sequence Diagram
        - The second for the Architecture Design

        Do not include any additional text. Just return the three code blocks.
        """

    def build_prompt(self, brain: 'Brain', user_input: str, previous_output: bool = False, previous_module: Optional[str] = None, goal: Goal = None, **kwargs) -> str:
        """
        Builds the prompt to generate UML diagrams and architecture designs.

        Parameters:
        - prd_text: Text from the PRD.

        Returns:
        - A formatted prompt string.
        """
        self.reset_prompt()
        self.prompt = f"""
        {self.base_prompt}
        
        User Input: 
        
        {user_input}
        
        Example PRD and Outputs:
        ----------------
        {self.examples}
        
        ----------------
        The examples above are for reference only. Your design should be based on the provided PRD.
        Ensure you provide as much detail as possible in your UML Class, UML Sequence, and Architecture Design, this will be more in depth than the examples provided and should be tailored to the PRD.

        PRD to Analyze (below):
        ----------------
        {brain.knowledge_base['prd']}
        ----------------

        Generate the three code block outputs as described above.  Ensure that prior to code block include the title of the output in markdown (i.e. # UML Class Diagram, # UML Sequence Diagram, or # Architecture Design)
        """
        return self.prompt


