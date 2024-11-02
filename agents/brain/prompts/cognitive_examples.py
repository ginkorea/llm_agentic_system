# cognitive_examples.py

from agents.brain.prompts.examples import ExamplesBase

class CognitiveExamples(ExamplesBase):
    def __init__(self):
        super().__init__()
        self.define_tool_examples()
        self.define_module_examples()

    def define_tool_examples(self):
        # Adding examples for specific tools within CognitiveBrain

        # Example for 'calculate' tool
        self.add_tool_example(
            user_input="calculate 100 / 4",
            tool_name="calculate",
            refined_prompt="100 / 4"
        )

        # Example for 'get_page' tool
        self.add_tool_example(
            user_input="fetch details from https://worldfacts.com",
            tool_name="get_page",
            refined_prompt="https://worldfacts.com"
        )

        # Example for 'search' tool
        self.add_tool_example(
            user_input="Search for recent research on cognitive science",
            tool_name="search",
            refined_prompt="recent research on cognitive science"
        )

        # Example for 'visualize_file_structure' tool
        self.add_tool_example(
            user_input="Visualize the file organization in my thesis project folder",
            tool_name="visualize_file_structure",
            refined_prompt="thesis project folder structure"
        )

    def define_module_examples(self):
        # Adding examples for specific lobes/modules within CognitiveBrain

        # Example for 'FrontalLobe'
        self.add_module_example(
            user_input="Explain the concept of neuroplasticity",
            lobe_index=1,  # FrontalLobe index in CognitiveBrain's module list
            refined_prompt="Explain neuroplasticity in cognitive terms."
        )

        # Example for 'TemporalLobe'
        self.add_module_example(
            user_input="Summarize the main findings of Freud's theories",
            lobe_index=2,  # TemporalLobe index
            refined_prompt="Provide a summary of Freud's main theories."
        )

        # Example for 'ParietalLobe'
        self.add_module_example(
            user_input="Calculate spatial reasoning needed for object placement",
            lobe_index=3,  # ParietalLobe index
            refined_prompt="Compute spatial requirements for object placement."
        )

        # Example for 'OccipitalLobe'
        self.add_module_example(
            user_input="Identify patterns in cognitive behavioral data",
            lobe_index=4,  # OccipitalLobe index
            refined_prompt="Analyze patterns in cognitive behavioral data."
        )

        # Example for 'BrocasArea'
        self.add_module_example(
            user_input="Generate a speech outline for cognitive science symposium",
            lobe_index=5,  # BrocasArea index
            refined_prompt="Outline speech for cognitive science symposium."
        )

# Example instantiation and retrieval
if __name__ == "__main__":
    cognitive_examples = CognitiveExamples()
    print(cognitive_examples.get_examples())
