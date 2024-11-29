from agents.brain.prompts.examples.base_examples import ExamplesBase


class UnitTestExamples(ExamplesBase):
    """
    Examples for Unit Test Generation.
    """

    def __init__(self):
        super().__init__()

    def get_examples(self) -> str:
        return f"""
        # Example PRD: 
        {self.get_prd()}
        
        # Example UML Class Diagram:
        {self.get_uml_class()}
        
        # Example Code
        {self.get_code_output()}

        # Example Unit Test Code
        {self.get_unit_test()}
        """
