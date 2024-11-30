from agents.brain.prompts.structured.structured_prompt import StructuredPrompt
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from agents.brain.core import Brain


class UnitTestPrompt(StructuredPrompt):
    """
    Specialized prompt for generating unit tests.
    """

    def __init__(self, tools=None, modules=None, examples=None, goal=None):
        super().__init__(tools=tools, modules=modules, examples=examples, goal=goal)
        self.base_prompt = """
        You are an expert in Python testing and software quality assurance. Your task is to generate unit tests 
        for the provided Python codebase. Each test must:
        - Cover individual methods or classes from the codebase.
        - Align with the PRD and UML Class Diagram.
        - Ensure comprehensive testing of inputs, outputs, and edge cases.
        - Follow the unittest framework and proper test structure.

        Include one test file per class or module, naming them as `test_<module_name>.py`.
        
        For importing modules, you should prefix the module with "workbench." plus the module name. Because all files are in the workbench directory.
        Do not prefix filenames with "workbench.".
        """

    def build_prompt(self, brain: 'Brain', prompt_input: str, **kwargs) -> str:
        """
        Builds the prompt for generating unit tests.

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

        Code Files:
        ----------------
        {brain.knowledge_base.get("code", "No code files found.")}

        ----------------

        Generate unit tests for each component as described above.
        """
        return self.prompt
