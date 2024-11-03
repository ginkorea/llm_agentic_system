# structured_prompt.py

from typing import Optional

class StructuredPrompt:
    """
    Base class for creating structured prompts for different brain modules (lobes).
    Initializes with optional tool descriptions, module descriptions, and examples.
    Allows flexible prompt construction, with support for building on previous output.
    """

    def __init__(self, tools: Optional[str] = None, modules: Optional[str] = None,
                 examples: Optional[str] = None):
        self.tools = tools or "No tools available."
        self.modules = modules or "No modules available."
        self.examples = examples or "No examples provided."
        self.base_prompt = "You are a brain module, responsible for handling specific task as part of a larger system. Respond to the following prompt based on the input."
        self.prompt = self.base_prompt  # Initialize prompt to base prompt

    def build_prompt(self, prompt_input: str, previous_output: bool = False, previous_module: Optional[str] = None) -> str:
        """
        Constructs the prompt based on user input, tools, modules, and examples.
        If `previous_output` is True, formats the prompt to incorporate previous output.

        Parameters:
        - prompt_input: The original input from the user or task.
        - previous_output: If True, incorporates previous module's output for chaining.
        - previous_module: The name of the previous module, if chaining prompts.

        Returns:
        - A formatted prompt string ready for the LLM.
        """
        self.reset_prompt()  # Start with a fresh prompt

        # Build prompt based on chaining or new input
        if previous_output:
            self.prompt += f"""
            React to the following output from the {previous_module} module:
            ----------------
            {prompt_input}
            ----------------
            """
        else:
            self.prompt += f"""
            React to the following input: "{prompt_input}"
            """
        return self.prompt

    def reset_prompt(self) -> None:
        """
        Resets the prompt to the base prompt.
        """
        self.prompt = self.base_prompt


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
            "refined_prompt": "<refined_prompt_for_lobe>"
        }}
        ----------------
        """
        self.reset_prompt()  # Initialize prompt to Controller's base prompt

