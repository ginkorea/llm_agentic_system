from agents.brain.prompts.structured.structured_prompt import StructuredPrompt

class AcceptanceTestGeneratorPrompt(StructuredPrompt):
    """
    Prompt class for generating both acceptance tests and unit tests.
    """

    def __init__(self, tools=None, modules=None, examples=None, goal=None):
        super().__init__(tools=tools, modules=modules, examples=examples, goal=goal)
        self.base_prompt = """
        You are tasked with generating tests to validate the system's functionality.
        - Write acceptance tests for end-to-end functionality.
        - Do not test individual components, but rather the system as a whole, unit tests will handle that.
        """

    def build_prompt(self, prompt_input: str, **kwargs) -> str:
        """
        Builds the prompt for generating both acceptance and unit tests.

        Parameters:
        - prompt_input: System description or requirements.

        Returns:
        - A formatted prompt string.
        """
        self.reset_prompt(goal=kwargs.get("goal"))
        self.prompt += f"""
        {self.base_prompt}

        Examples for Acceptance Tests:
        ----------------
        {self.examples}
        
        ----------------
        
        # the examples above are examples of PRD, UML, Architecture, and Acceptance Tests
        # generate acceptance tests based on the input below using the examples above as a guide
        
        ----------------

        Input Data for Tests:
        ----------------
        {prompt_input}

        Generate the acceptance tests and unit tests as described above.
        """
        return self.prompt
