from agents.brain.prompts.examples.base_examples import ExamplesBase

class AcceptanceTestGeneratorExamples(ExamplesBase):
    """
    Examples for AcceptanceTestGenerator, retrieving PRD, UML, Architecture, and Acceptance Test examples.
    """

    def __init__(self):
        super().__init__()

    def get_examples(self) -> str:
        examples_string = f"PRD Examples:\n{self.get_prd()}\n\nUML Examples:\n{self.get_uml()}\n\nArchitecture Examples:\n{self.get_architecture()}\n\nAcceptance Test Examples:\n{self.get_acceptance_test()}"
        return examples_string