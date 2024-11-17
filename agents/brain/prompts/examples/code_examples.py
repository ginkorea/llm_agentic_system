from agents.brain.prompts.examples import ExamplesBase

class CodeExamples(ExamplesBase):
    """
    Examples for the CodeBrain model, including tools and modules.
    """

    def __init__(self):
        super().__init__()
        self.define_tool_examples()
        self.define_module_examples()

    def define_tool_examples(self):
        # Adding examples for specific tools within CodeBrain

        # Example for 'search' tool
        self.add_tool_example(
            user_input="Find Python libraries for data visualization",
            tool_name="search",
            refined_prompt="Python libraries for data visualization"
        )

        # Example for 'calculate' tool
        self.add_tool_example(
            user_input="What is 25 times 4?",
            tool_name="calculate",
            refined_prompt="25 * 4"
        )

        # Example for 'get_page' tool
        self.add_tool_example(
            user_input="Fetch the webpage content of https://example.com",
            tool_name="get_page",
            refined_prompt="https://example.com"
        )

        # Example for 'visualize_file_structure' tool
        self.add_tool_example(
            user_input="Show the directory structure of my project",
            tool_name="visualize_file_structure",
            refined_prompt="directory structure of project"
        )

    def define_module_examples(self):
        # Adding examples for specific modules/lobes in CodeBrain

        # Example for 'TaskRouter'
        self.add_module_example(
            user_input="Delegate tasks to appropriate lobes for software design",
            lobe_index=0,  # TaskRouter index in CodeBrain's module list
            refined_prompt="Route task to appropriate lobe for software design"
        )

        # Example for 'SoftwareDesigner'
        self.add_module_example(
            user_input="Generate UML diagram and architecture design for the PRD",
            lobe_index=1,  # SoftwareDesigner index
            refined_prompt="Create UML diagram and architecture design from PRD."
        )

        # Example for 'SoftwareDesignJudge'
        self.add_module_example(
            user_input="Evaluate the UML and architecture for compliance with PRD",
            lobe_index=2,  # SoftwareDesignJudge index
            refined_prompt="Assess UML and architecture against PRD requirements."
        )

        # Example for 'EnvironmentSetupManager'
        self.add_module_example(
            user_input="Generate requirements.txt and other setup files for the project",
            lobe_index=3,  # EnvironmentSetupManager index
            refined_prompt="Create environment setup files based on PRD and design."
        )

        # Example for 'GoalSetter'
        self.add_module_example(
            user_input="Define milestones for completing the software development goal",
            lobe_index=4,  # GoalSetter index
            refined_prompt="Set milestones for achieving the software development goal."
        )

# Example instantiation and retrieval
if __name__ == "__main__":
    code_examples = CodeExamples()
    print(code_examples.get_examples())
