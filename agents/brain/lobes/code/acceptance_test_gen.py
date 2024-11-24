from agents.brain.lobes.module import Module
from agents.brain.prompts.examples.acceptance_test_examples import AcceptanceTestGeneratorExamples
from agents.brain.prompts.structured.acceptance_test_prompt import AcceptanceTestGeneratorPrompt

class AcceptanceTestGenerator(Module):
    """
    Generates both acceptance tests and unit tests based on requirements.
    """

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=5,
            system_message="Generate Python tests for validating system functionality.",
        )
        self.examples = AcceptanceTestGeneratorExamples()
        self.prompt_builder = None

    def build_prompt_builder(self, brain=None, modules=None, tools=None, examples=None, **kwargs):
        """
        Initializes the prompt builder using AcceptanceTestGeneratorPrompt.
        """
        examples = self.examples.get_examples() if examples is None else examples
        self.prompt_builder = AcceptanceTestGeneratorPrompt(modules=modules, tools=tools, examples=examples, **kwargs)

    def generate_tests(self, requirements: str) -> str:
        """
        Generates both acceptance and unit tests based on provided requirements.

        Parameters:
        - requirements: System requirements or descriptions.

        Returns:
        - Generated Python test code as a string.
        """
        if not self.prompt_builder:
            self.build_prompt_builder()
        prompt = self.prompt_builder.build_prompt(requirements)
        return self.model.process(prompt)

    def process(self, requirements: str) -> str:
        """
        Processes the input requirements and generates Python test files.

        Parameters:
        - requirements: System requirements or descriptions.

        Returns:
        - Generated Python test code as a string.
        """
        return self.generate_tests(requirements)