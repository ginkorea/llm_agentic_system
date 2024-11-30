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

        Each file should include the following:
        - The filename and path as a comment (e.g., `# templates/index.html`).
        - The file content formatted correctly within code blocks.

        Ensure the filenames reflect their directory structure. For example:
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

        extended_prompt = f"""
        Analyze the provided PRD and Architecture Design:

        PRD:
        {brain.knowledge_base['prd']}

        Architecture Design:
        {brain.knowledge_base['architecture']}

        Ensure the following:
        - All filenames represent the correct directory structure.
        - File content is appropriately formatted.
        - Include a valid `requirements.txt` for Python dependencies.

        ---------------
        Example Outputs:
        {self.examples}
        ---------------
        """
        self.prompt += extended_prompt
        return self.prompt
