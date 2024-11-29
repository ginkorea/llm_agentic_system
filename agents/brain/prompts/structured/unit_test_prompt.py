from agents.brain.prompts.structured.structured_prompt import StructuredPrompt


class UnitTestPrompt(StructuredPrompt):
    """
    Specialized prompt for generating unit tests.
    """

    def __init__(self, tools=None, modules=None, examples=None, goal=None):
        super().__init__(tools=tools, modules=modules, examples=examples, goal=goal)
        self.base_prompt = """
        You are an expert in Python testing and software quality assurance. Your task is to generate unit tests 
        for the provided Python codebase. Each test must:
        - Cover individual methods or classes from the codebase.
        - Align with the PRD and UML Class Diagram.
        - Ensure comprehensive testing of inputs, outputs, and edge cases.
        - Follow the unittest framework and proper test structure.

        Include one test file per class or module, naming them as `test_<module_name>.py`.
        """

    def build_prompt(self, prompt_input: str, **kwargs) -> str:
        """
        Builds the prompt for generating unit tests.

        Parameters:
        - prompt_input: Context for the prompt.
        """
        self.reset_prompt(goal=None)
        self.prompt += f"""
        {self.base_prompt}

        Examples:
        ----------------
        {self.examples}

        ----------------

        PRD: 
        {kwargs.get("prd", "PRD not found")}    

        UML Class Diagram:
        {kwargs.get("uml_class", "UML Class Diagram not found")}

        Code Files:
        ----------------
        {kwargs.get("code_files", "No code files found.")}

        ----------------

        Generate unit tests for each component as described above.
        """
        return self.prompt
