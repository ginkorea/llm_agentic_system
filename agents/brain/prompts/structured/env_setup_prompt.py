from seobject import kwargs

from agents.brain.prompts.structured import StructuredPrompt
from agents.brain.goal.goal import Goal
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from agents.brain.core import Brain

class EnvironmentSetupPrompt(StructuredPrompt):
    """
    Specialized prompt class for generating dynamic frontend and backend artifacts.
    """

    def __init__(self, examples=None):
        super().__init__(examples=examples)
        self.base_prompt = """
        You are an environment setup expert. Your task is to analyze the provided PRD, and Architecture Design to generate:
        - A requirements.txt file listing Python dependencies for the backend.
        - Frontend artifacts like HTML, CSS, and JavaScript files.

        The output should include properly formatted code blocks with filenames as comments.
        """


    def build_prompt(self, brain: 'Brain', prompt_input: str, previous_output: bool = False, previous_module: Optional[str] = None, goal: Goal = None) -> str:
        """
        Builds the prompt to generate environment setup files.

        Parameters:
        - prompt_input: Text from the PRD, UML diagram, and architecture design.

        Returns:
        - A formatted prompt string.
        """
        self.reset_prompt()
        self.prompt = self.base_prompt

        extended_prompt = f"""
        Prompt Input: 
        
        {prompt_input}
        
        ---------------
        
        Example PRD Architecture Design, and Outputs:
        
        ----------------
        
        {self.examples}

        ----------------

        PRD and Architecture Design to Analyze:
        
        ----------------
        
        PRD: {brain.knowledge_base['prd']}
        
        Architecture: {brain.knowledge_base['architecture']}
        
        ----------------

        Generate the outputs as described above.
        """

        self.prompt += extended_prompt
        return self.prompt

