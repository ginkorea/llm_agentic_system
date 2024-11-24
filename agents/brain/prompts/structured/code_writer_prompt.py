# code_writer_prompt.py

from agents.brain.prompts.structured.structured_prompt import StructuredPrompt
from typing import Optional

class CodeWriterPrompt(StructuredPrompt):
    """
    Specialized prompt for generating Python files based on PRD, UML Diagram, and Architecture Design.
    """

    def __init__(self, tools=None, modules=None, examples=None, goal=None):
        super().__init__(tools=tools, modules=modules, examples=examples, goal=goal)
        self.base_prompt = """
        You are a code generation expert. Your task is to analyze the PRD, UML Diagram, and Architecture Design to generate:
        - One Python file per class described in the UML Diagram.
        - A `main.py` file integrating all classes.

        Each output should be a properly formatted Python code block with the filename as a comment at the top.
        """

    def build_prompt(self, prompt_input: str, previous_output: bool = False,
                     previous_module: Optional[str] = None, goal=None, **kwargs) -> str:
        """
        Builds the prompt for generating Python code files.

        Parameters:
        - prompt_input: Input text combining PRD, UML, and Architecture Design.
        """
        self.reset_prompt(goal=goal)
        self.prompt += f"""
        {self.base_prompt}

        Examples:
        ----------------
        {self.examples}

        ----------------

        Input Data:
        ----------------
        {prompt_input}

        Generate the Python code files as described above.
        """
        return self.prompt
