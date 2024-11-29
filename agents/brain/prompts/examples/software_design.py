# software_design_examples.py

from agents.brain.prompts.examples import ExamplesBase

class SoftwareDesignExamples(ExamplesBase):
    """
    Examples for the SoftwareDesignLobe, focused on generating UML diagrams and architecture designs.
    """

    def __init__(self):
        super().__init__()

    def get_examples(self) -> str:
        """
        Concatenates the PRD example, UML output, and architecture design into one string.
        """
        return f"{self.get_prd()}\n\n{self.get_uml()}\n\n{self.get_architecture()}"
