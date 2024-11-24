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
            memory_limit=5,
            system_message="Analyze the PRD, UML Diagram, and Architecture Design to generate Python code files.",
        )
        self.examples = CodeWriterExamples()
        self.prompt_builder = None

    def build_prompt_builder(self, brain=None, modules=None, tools=None, examples=None, **kwargs):
        """
        Initializes the prompt builder using the CodeWriterPrompt class.
        """
        examples = self.examples.get_examples() if examples is None else examples
        self.prompt_builder = CodeWriterPrompt(modules=modules, tools=tools, examples=examples, **kwargs)

    def generate_code(self, prd: str, uml: str, architecture: str) -> str:
        """
        Generates Python code files.

        Parameters:
        - prd: Product Requirements Document text.
        - uml: UML Diagram text.
        - architecture: Architecture Design text.

        Returns:
        - Generated Python code as a string.
        """
        if not self.prompt_builder:
            self.build_prompt_builder()
        prompt_input = f"# PRD\n{prd}\n\n# UML\n{uml}\n\n# Architecture\n{architecture}"
        prompt = self.prompt_builder.build_prompt(prompt_input)
        return self.model.process(prompt)


# Test the CodeWriter module with sample PRD, UML, and Architecture Design

if __name__ == "__main__":
    from const.sk import kc as sk
    code_writer = CodeWriter()
    code_writer.build_prompt_builder()
    print("\nGenerated Output:\n")
    print(code_writer.prompt_builder.build_prompt("Sample PRD, UML, and Architecture Design text."))