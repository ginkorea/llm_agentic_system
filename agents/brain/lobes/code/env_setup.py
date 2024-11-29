from agents.brain.prompts.examples.env_setup_examples import EnvironmentSetupExamples
from agents.brain.prompts.structured.env_setup_prompt import EnvironmentSetupPrompt
from agents.brain.lobes.module import Module
from typing import Optional
from agents.brain.core import Brain


class EnvironmentSetupManager(Module):
    """Handles the environment setup phase, generating dynamic frontend and backend artifacts."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=3,
            system_message="You analyze the PRD, UML Diagram, and Architecture Design to generate environment setup files like requirements.txt and frontend artifacts.",
        )
        self.examples = EnvironmentSetupExamples()
        self.prompt_input = None

    def build_prompt_builder(self, brain: Optional[Brain] = None, modules=None, tools=None, examples=None, raw_output=None):
        """
        Builds a structured prompt builder specific to the EnvironmentSetupManager.
        Uses the brain's knowledge base with keys `prd`, `uml`, and `architecture` to format the prompt input.
        """
        try:
            if brain and brain.knowledge_base:
                prd = brain.knowledge_base.get("prd", "").strip()
                uml = brain.knowledge_base.get("uml", "").strip()
                architecture = brain.knowledge_base.get("architecture", "").strip()

                if not prd:
                    raise ValueError("PRD data is missing from the knowledge base.")
                if not uml:
                    raise ValueError("UML Diagram data is missing from the knowledge base.")
                if not architecture:
                    raise ValueError("Architecture Design data is missing from the knowledge base.")

                # Format the combined input for the prompt
                formatted_input = f"""
                # PRD
                {prd}
    
                # UML Diagram
                {uml}
    
                # Architecture Design
                {architecture}
                """
                self.prompt_input = formatted_input
        except ValueError as e:
            print(f"Error in EnvironmentSetupManager.build_prompt_builder: {e}")

        self.prompt_builder = EnvironmentSetupPrompt(examples=self.examples.get_examples())


    def process_input(self, brain: Brain) -> str:
        """
        Processes the PRD, UML Diagram, and Architecture Design to generate dynamic artifacts.

        Parameters:
        - brain: The Brain instance containing the knowledge base.

        Returns:
        - The generated environment setup files as a single string.
        """
        # Ensure the prompt builder is initialized
        self.build_prompt_builder(brain=brain)

        # Generate environment setup files using LLM
        _output = self.prompt_builder.build_prompt(self.prompt_input)
        generated_artifacts = self.model.invoke(_output)

        return generated_artifacts.content.strip()


