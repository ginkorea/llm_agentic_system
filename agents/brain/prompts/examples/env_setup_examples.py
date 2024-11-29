# env_setup_examples.py

from agents.brain.prompts.examples import ExamplesBase

class EnvironmentSetupExamples(ExamplesBase):
    """
    Examples for the EnvironmentSetupManager, focused on generating dependency files.
    """

    def get_examples(self) -> str:
        """
        Concatenates the PRD example and requirements.txt example into one string.
        """
        examples_string = (f"PRD Example:\n"
                           f"{self.get_prd()}\n\n"
                           f"Requirements.txt Example:\n"
                           f"{self.get_requirements_txt()}")

        return examples_string
