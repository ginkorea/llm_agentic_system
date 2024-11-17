from typing import Optional
from agents.brain.prompts.structured import StructuredPrompt

class ControllerPrompt(StructuredPrompt):
    """
    Specialized prompt class for the controller module, with specific formatting for tools,
    modules, and examples relevant to the controller's functionality.
    """

    def __init__(self, tools: Optional[str] = None, modules: Optional[str] = None,
                 examples: Optional[str] = None):
        super().__init__(tools, modules, examples)
        self.base_prompt = f"""
        You are the control center for the brain, responsible for reflexive thinking and traffic routing.
        You have access to various tools and specialized modules (lobes) to handle tasks.
        Respond in JSON format to indicate whether a tool or a lobe should handle the task.

        Available tools:
        {self.tools}

        Available brain lobes (llm modules):
        {self.modules}

        Based on the user's input, decide whether to use a tool or a lobe to handle the task.

        ----------------
        Prompt Examples:

        {self.examples}

        ----------------

        Please respond in JSON format:
        - If using a tool:
        {{
            "use_tool": true,
            "tool_name": "<tool_name>",
            "refined_prompt": "<refined_prompt_for_tool>"
        }}
        - If using a lobe:
        {{
            "use_tool": false,
            "lobe_index": <lobe_index>,
            "refined_prompt": "<full original prompt> + '|' + <refined_prompt_for_lobe>"
        }}
        ----------------
        """
        self.reset_prompt()  # Initialize prompt to Controller's base prompt