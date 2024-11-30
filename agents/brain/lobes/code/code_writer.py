# code_writer.py

from agents.brain.lobes.module import Module
from agents.brain.prompts.examples.code_writer_examples import CodeWriterExamples
from agents.brain.prompts.structured.code_writer_prompt import CodeWriterPrompt

class CodeWriter(Module):
    """
    Handles the code generation phase, producing Python files based on PRD, UML Diagram, and Architecture Design.
    """

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=10,
            system_message="Analyze the PRD, UML Diagram, Architecture Design, Required Classes, and Existing Code Base "
                           " to generate Python code files.",
        )
        self.examples = CodeWriterExamples()
        self.prompt_builder = None

    def build_prompt_builder(self, brain=None, modules=None, tools=None, examples=None, raw_output=None):
        """
        Initializes the prompt builder using the CodeWriterPrompt class.
        """

        self.prompt_builder = CodeWriterPrompt(examples=self.examples.get_examples())
