from agents.brain.prompts.examples.base_examples import ExamplesBase


class AcceptanceTestExamples(ExamplesBase):
    """
    Examples for Acceptance Test Generation.
    """

    def __init__(self):
        super().__init__()

    def get_examples(self) -> str:
        return f"""
        # Example PRD: 
        {self.get_prd()}
        
        # Example UML Class Diagram:
        {self.get_uml_class()}
        
        # Example Code: 
        {self.get_code_output()}
        
        # Example Acceptance Test Code
        {self.get_acceptance_test()}
        """
