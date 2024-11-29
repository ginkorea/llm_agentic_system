from agents.brain.prompts.examples.base_examples import ExamplesBase

class CodeWriterExamples(ExamplesBase):
    """
    Examples for CodeWriter, retrieving PRD, UML, and Architecture examples with optional nesting.
    """

    def __init__(self):
        super().__init__()

    def get_examples(self) -> str:
        examples_string = f"PRD Examples:\n{self.get_prd()}\n\nUML Examples:\n{self.get_uml()}\n\nArchitecture Examples:\n{self.get_architecture()}"
        code_examples = f"\nCode Examples: {self.get_code_output()}"
        examples_string += code_examples
        return examples_string
