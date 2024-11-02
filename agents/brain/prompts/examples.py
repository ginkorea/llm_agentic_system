import json

class ExamplesBase:
    """Base class for defining examples used in prompt generation."""

    def __init__(self):
        self.tool_examples = []
        self.module_examples = []

    def add_tool_example(self, user_input: str, tool_name: str, refined_prompt: str):
        """Add a tool example to the list of tool examples."""
        example = {
            "use_tool": True,
            "tool_name": tool_name,
            "refined_prompt": refined_prompt
        }
        self.tool_examples.append(self.format_example(user_input, example))

    def add_module_example(self, user_input: str, lobe_index: int, refined_prompt: str):
        """Add a module example to the list of module examples."""
        example = {
            "use_tool": False,
            "lobe_index": lobe_index,
            "refined_prompt": refined_prompt
        }
        self.module_examples.append(self.format_example(user_input, example))

    @staticmethod
    def format_example(user_input: str, response: dict) -> str:
        """Helper to format an example entry."""
        response_str = json.dumps(response, indent=4)
        return f"User input: \"{user_input}\"\nResponse:\n{response_str}\n"

    def get_examples(self) -> str:
        """Return a formatted string of examples for both tools and modules."""
        examples_str = "\n".join(self.tool_examples + self.module_examples)
        return examples_str if examples_str else "No examples available."
