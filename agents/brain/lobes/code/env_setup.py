from agents.brain.prompts.examples.env_setup_examples import EnvironmentSetupExamples
from agents.brain.prompts.structured.env_setup_prompt import EnvironmentSetupPrompt
from agents.brain.lobes.module import Module
from typing import Optional
from agents.brain.core import Brain


class EnvironmentRequirementsDeveloper(Module):
    """Handles the environment setup phase, generating dynamic frontend and backend artifacts."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=3,
            system_message="Tool to generate the requirements to initialize the virtual environment from the PRD, UML Diagrams, and Architecture.",
        )
        self.examples = EnvironmentSetupExamples()
        self.prompt_input = None

    def build_prompt_builder(self, brain: Optional[Brain] = None, modules=None, tools=None, examples=None, raw_output=None):
        """
        Builds a structured prompt builder specific to the EnvironmentSetupManager.
        Uses the brain's knowledge base with keys `prd`, `uml`, and `architecture` to format the prompt input.
        """


        self.prompt_builder = EnvironmentSetupPrompt(examples=self.examples.get_examples())






