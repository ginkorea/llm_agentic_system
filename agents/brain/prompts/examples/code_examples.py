from agents.brain.prompts.examples import ExamplesBase

class CodeExamples(ExamplesBase):
    def __init__(self):
        super().__init__()
        self.define_tool_examples()
        self.define_module_examples()

    def define_tool_examples(self):
        # Adding examples for specific tools within CodeBrain

        # Example for 'calculate' tool
        self.add_tool_example(
            user_input="calculate 10 * 5",
            tool_name="calculate",
            refined_prompt="10 * 5"
        )

        # Example for 'get_page' tool
        self.add_tool_example(
            user_input="fetch content from https://example.com",
            tool_name="get_page",
            refined_prompt="https://example.com"
        )

        # Example for 'search' tool
        self.add_tool_example(
            user_input="Find the latest Python tutorials online",
            tool_name="search",
            refined_prompt="latest Python tutorials"
        )

        # Example for 'visualize_file_structure' tool
        self.add_tool_example(
            user_input="Show me the file structure of my project directory",
            tool_name="visualize_file_structure",
            refined_prompt="project directory structure"
        )

    def define_module_examples(self):
        # Adding examples for specific lobes/modules within CodeBrain

        # Example for 'LogicLobe'
        self.add_module_example(
            user_input="Generate the main logic for a function that sorts a list",
            lobe_index=1,  # LogicLobe index in CodeBrain's module list
            refined_prompt="Create main logic for a list-sorting function."
        )

        # Example for 'DebuggerLobe'
        self.add_module_example(
            user_input="Debug the function to identify why it returns None",
            lobe_index=2,  # DebuggerLobe index
            refined_prompt="Analyze the function for potential reasons it returns None."
        )

        # Example for 'SeniorDev'
        self.add_module_example(
            user_input="Resolve complex issue in recursive function causing stack overflow",
            lobe_index=3,  # SeniorDev index
            refined_prompt="Examine recursive function to fix stack overflow error."
        )

        # Example for 'SyntaxLobe'
        self.add_module_example(
            user_input="Generate the correct syntax for a Python dictionary comprehension",
            lobe_index=4,  # SyntaxLobe index
            refined_prompt="Generate syntax for a dictionary comprehension in Python."
        )

        # Example for 'DocumentationLobe'
        self.add_module_example(
            user_input="Add documentation to the sorting function",
            lobe_index=5,  # DocumentationLobe index
            refined_prompt="Create documentation for the sorting function."
        )

        # Example for 'TestingLobe'
        self.add_module_example(
            user_input="Write unit tests for the list sorting function",
            lobe_index=6,  # TestingLobe index
            refined_prompt="Generate unit tests to validate list sorting function."
        )

        # Example for 'OptimizerLobe'
        self.add_module_example(
            user_input="Optimize the sort function for better performance",
            lobe_index=7,  # OptimizerLobe index
            refined_prompt="Enhance performance of the sorting function."
        )

        # Example for 'RefactorLobe'
        self.add_module_example(
            user_input="Refactor the code to improve readability",
            lobe_index=8,  # RefactorLobe index
            refined_prompt="Refactor code to enhance readability."
        )

# Example instantiation and retrieval
if __name__ == "__main__":
    code_examples = CodeExamples()
    print(code_examples.get_examples())
