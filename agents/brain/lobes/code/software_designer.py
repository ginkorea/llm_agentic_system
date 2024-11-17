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
            temperature=0.5,
            memory_limit=3,
            system_message="You generate UML diagrams and architecture designs based on the provided PRD.",
        )
        self.examples = SoftwareDesignExamples()

    def build_prompt_builder(self, brain: Optional['Brain'] = None, modules=None, tools=None, examples=None):
        """
        Builds a structured prompt builder specific to the SoftwareDesignLobe.
        """
        self.prompt_builder = SoftwareDesignPrompt(examples=self.examples.get_examples())

    def process_input(self, prd_text: str) -> str:
        """
        Simulates processing the input PRD and generating UML and architecture outputs.

        Parameters:
        - prd_text: The Product Requirements Document (PRD) input.

        Returns:
        - The generated UML and architecture design as a single string.
        """
        self.build_prompt_builder()
        return self.prompt_builder.build_prompt(prd_text)


# Test the SoftwareDesignLobe with a sample PRD
if __name__ == "__main__":
    # Initialize the lobe
    from const.sk import kc as sk
    software_design_lobe = SoftwareDesigner()

    # Sample PRD input
    sample_prd = """
    # Project Overview
    The `Task Tracker` application is designed to streamline task management for small teams, enabling members to create, assign, and track tasks with real-time updates. The system focuses on simplicity and efficiency.

    # Features
    1. **Task Management**: Users can create, assign, and update tasks with descriptions, priorities, and deadlines.
    2. **Team Collaboration**: Each team has a dashboard showing task status and team activity.
    3. **Notifications**: Alerts for approaching deadlines and task updates.

    # Constraints
    - Must support both desktop and mobile devices.
    - The system should handle up to 100 simultaneous users.

    # Technical Details
    - **Frontend**: ReactJS for cross-platform compatibility.
    - **Backend**: Node.js for task management APIs.
    - **Database**: PostgreSQL for secure and structured data storage.

    # Use Cases
    1. A team lead assigns tasks to members with deadlines and priorities.
    2. Team members update task progress and set task statuses to `In Progress` or `Complete`.
    3. A user receives notifications for approaching deadlines and task changes.
    """

    # Generate and display the output
    prompt_output = software_design_lobe.process_input(sample_prd)
    print("Generated Prompt:\n")
    print(prompt_output)
    output = software_design_lobe.model.invoke(prompt_output)
    print("\nGenerated Output:\n")
    print(output.content)

