from agents.brain.prompts.structured import StructuredPrompt
from agents.brain.goal.goal import Goal
from typing import Optional

class EnvironmentSetupPrompt(StructuredPrompt):
    """
    Specialized prompt class for generating dynamic frontend and backend artifacts.
    """

    def __init__(self, examples=None):
        super().__init__(examples=examples)
        self.base_prompt = """
        You are an environment setup expert. Your task is to analyze the provided PRD, UML Diagram, and Architecture Design to generate:
        - A requirements.txt file listing Python dependencies for the backend.
        - A package.json or equivalent file for the frontend, if applicable.
        - Any additional setup files needed for the project.

        The output should include properly formatted code blocks with filenames as comments.
        """

    def build_prompt(self, prompt_input: str, previous_output: bool = False, previous_module: Optional[str] = None, goal: Goal = None) -> str:
        """
        Builds the prompt to generate environment setup files.

        Parameters:
        - prompt_input: Text from the PRD, UML diagram, and architecture design.

        Returns:
        - A formatted prompt string.
        """
        return f"""
        {self.base_prompt}

        Example PRD, UML Diagram, Architecture Design, and Outputs:
        ----------------
        {self.examples}

        ----------------

        PRD, UML Diagram, and Architecture Design to Analyze:
        ----------------
        {prompt_input}
        ----------------

        Generate the outputs as described above.
        """

