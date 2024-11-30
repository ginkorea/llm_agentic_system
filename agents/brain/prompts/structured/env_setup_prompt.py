from typing import Optional
from agents.brain.prompts.structured import StructuredPrompt
from agents.brain.goal.goal import Goal

class EnvironmentSetupPrompt(StructuredPrompt):
    """
    Specialized prompt class for generating environment setup artifacts.
    """

    def __init__(self, examples=None):
        super().__init__(examples=examples)
        self.base_prompt = """
        You are an environment setup expert. Your task is to analyze the provided PRD and Architecture Design to generate:
        - A `requirements.txt` file listing Python dependencies for the backend.
        - Frontend artifacts like HTML, CSS, and JavaScript files.
        - Any additional backend setup files.

        Each file must include:
        - The filename and path as a comment (e.g., `# templates/index.html`).
        - The file content formatted correctly within code blocks.

        Ensure filenames reflect their directory structure. For example:
        - `templates/index.html`
        - `static/css/styles.css`
        - `static/js/app.js`
        - `requirements.txt`
        """

    def build_prompt(self, brain, prompt_input: str, previous_output: bool = False, previous_module: Optional[str] = None, goal: Goal = None) -> str:
        """
        Builds the prompt to generate environment setup files.

        Parameters:
        - brain: The Brain instance containing knowledge.
        - prompt_input: Text from the PRD and Architecture Design.

        Returns:
        - A formatted prompt string.
        """
        self.reset_prompt()
        self.prompt = self.base_prompt

        prd = brain.knowledge_base.get('prd', "No PRD available.")
        architecture = brain.knowledge_base.get('architecture', "No Architecture available.")

        extended_prompt = f"""
        Analyze the provided PRD and Architecture Design:

        PRD:
        {prd}

        Architecture Design:
        {architecture}

        Ensure:
        - All filenames represent the correct directory structure.
        - File content is appropriately formatted.
        - Include a valid `requirements.txt` for Python dependencies!!!! This is crucial.
        
        Do Not: 
        - Include any trailing explanations or comments after the code.
        - Include any unnecessary files or artifacts.
        - Try to implement the code based on the PRD or Architecture Design.
        
        ---------------
        Example Outputs:
        {self.examples}
        ---------------
        
        The format of the requirements.txt file is critical and will be validated.  Follow this format exactly:
        - Each line should contain a package name and version, separated by `==`.
        - Comments should be prefixed with `#`.
        - Include only necessary dependencies.
        - Do not include any unnecessary packages.
        - Do not include any trailing comments or explanations.
        example:
        # requirements.txt
        ```plaintext
        Flask==2.0.1
        Flask-Cors==3.0.10
        ```
        """
        self.prompt += extended_prompt
        return self.prompt
