from agents.brain.prompts.structured.structured_prompt import StructuredPrompt
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from agents.brain.core import Brain


class AcceptanceTestPrompt(StructuredPrompt):
    """
    Specialized prompt for generating acceptance tests.
    """

    def __init__(self, tools=None, modules=None, examples=None, goal=None):
        super().__init__(tools=tools, modules=modules, examples=examples, goal=goal)
        self.base_prompt = """
        You are an expert in Python testing and software verification. Your task is to generate comprehensive acceptance tests for the provided system. 
        These tests must validate system functionality against the PRD, UML Class Diagram, and Architecture Design.

        Each test must:
        - Validate key functionality as described in the PRD.
        - Ensure all classes and methods align with the UML Class Diagram.
        - Verify compliance with the Architecture Design.
        - Follow the unittest framework.

        Include one test file per component and ensure the main flow is tested in a separate `test_main.py` file.
        """

    def build_prompt(self, brain: 'Brain', prompt_input: str, **kwargs) -> str:
        """
        Builds the prompt for generating acceptance tests.

        Parameters:
        - prompt_input: Context for the prompt.
        """
        self.reset_prompt(goal=None)
        self.prompt += f"""
        {self.base_prompt}

        Examples:
        ----------------
        {self.examples}

        ----------------

        PRD: 
        {brain.knowledge_base.get("prd", "PRD not found")}    

        UML Class Diagram:
        {brain.knowledge_base.get("uml_class", "UML Class Diagram not found")}

        Architecture Design:
        {brain.knowledge_base.get("architecture", "Architecture Design not found")}

        Code Files:
        ----------------
        {brain.knowledge_base.get("code_files", "No code files found.")}

        ----------------

        Generate acceptance tests as described above.
        """
        return self.prompt
