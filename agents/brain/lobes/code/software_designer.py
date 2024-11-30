from agents.brain.prompts.examples import SoftwareDesignExamples
from agents.brain.prompts.structured import SoftwareDesignPrompt
from agents.brain.lobes.module import Module
from typing import Optional
from agents.brain.core import Brain


class SoftwareDesigner(Module):
    """Handles the design phase, generating UML diagrams and architecture designs from PRD input."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.3,
            memory_limit=3,
            system_message="You generate UML diagrams and architecture designs based on the provided PRD.",
        )
        self.examples = SoftwareDesignExamples()

    def build_prompt_builder(self, brain: Optional['Brain'] = None, modules=None, tools=None, examples=None, raw_output=None):
        """
        Builds a structured prompt builder specific to the SoftwareDesignLobe.
        """
        self.prompt_builder = SoftwareDesignPrompt(examples=self.examples.get_examples())



# Test the SoftwareDesignLobe with a sample PRD
if __name__ == "__main__":
    # Initialize the lobe
    from const.sk import kc as sk
    software_design_lobe = SoftwareDesigner()

    # Sample PRD input
    sample_prd_file = '/workbench/PRD.md'
    with open(sample_prd_file, 'r') as file:
        sample_prd = file.read()

    # Generate and display the output
    prompt_output = software_design_lobe.process(sample_prd)
    print("\nGenerated Output:\n")
    print(prompt_output)

