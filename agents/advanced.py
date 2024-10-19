from agents.base import Agent
from agents.brain.memory.ov_embedded import OpenvinoMemoryWithEmbeddings
from agents.brain.memory.cuda_embedded import CudaMemoryWithEmbeddings
import json

class AdvancedAgent(Agent):
    def __init__(self, memory_type: str = 'openvino'):
        super().__init__()  # Initialize base Agent attributes
        # Generate tool descriptions for use in prompts
        self.tool_descriptions = {tool.name: tool.description for tool in self.toolkit.tools}
        # Initialize memory with embeddings
        if memory_type == 'openvino':
            self.brain.memory = OpenvinoMemoryWithEmbeddings(forget_threshold=10)
        else:
            self.brain.memory = CudaMemoryWithEmbeddings(forget_threshold=10)

    def advanced_determine_action(self, user_input: str) -> (bool, int, str, str):
        """
        Use the brain's PreFrontalCortex to determine if the input should
        be handled by a tool or an LLM.

        Returns:
            - (True, tool_index, tool_name, refined_prompt) if a tool should be used
            - (False, -1, lobe_name, refined_prompt) if an LLM should be used
        """
        # Build tool information string for the prompt
        tool_info = "\n".join([f"{name}: {desc}" for name, desc in self.tool_descriptions.items()])

        # **Include examples in the prompt**
        examples = """
Examples:

User input: "calculate 5 + 5"
Response:
{
    "use_tool": true,
    "tool_name": "calculate",
    "refined_prompt": "5 + 5"
}

User input: "get_page https://www.google.com"
Response:
{
    "use_tool": true,
    "tool_name": "get_page",
    "refined_prompt": "https://www.google.com"
}

User input: "What is the capital of France?"
Response:
{
    "use_tool": false,
    "lobe_name": "FrontalLobe",
    "refined_prompt": "What is the capital of France?"
}
"""

        # Construct the prompt for the PreFrontalCortex
        prompt = f"""
You are an intelligent agent with the following tools at your disposal:
{tool_info}

Based on the following user input, determine whether the input is best handled by one of the tools or by generating a direct response using the LLM.

{examples}

For tool usage, respond in JSON format:
{{
    "use_tool": true,
    "tool_name": "<tool_name>",
    "refined_prompt": "<refined_prompt_for_tool>"
}}

For LLM usage, respond in JSON format:
{{
    "use_tool": false,
    "lobe_name": "<lobe_name>",
    "refined_prompt": "<refined_prompt_for_llm>"
}}

User input: {user_input}
"""

        # Use the PreFrontalCortex to process the decision
        prefrontal_cortex = self.brain.get_lobe_by_name("PreFrontalCortex")

        # Pass the memory DataFrame directly; it will be handled in the Lobe class
        memory = self.brain.memory.short_term_df

        decision_response = prefrontal_cortex.process(user_input=prompt, memory=memory)

        # Parse the JSON response from the PreFrontalCortex
        try:
            decision = json.loads(decision_response)
        except json.JSONDecodeError:
            # If parsing fails, default to using the FrontalLobe for LLM response
            return False, -1, 'FrontalLobe', user_input

        if decision.get('use_tool'):
            tool_name = decision.get('tool_name')
            refined_prompt = decision.get('refined_prompt', user_input)
            # Find the tool index based on the tool name
            for idx, tool in enumerate(self.toolkit.tools):
                if tool.name == tool_name:
                    return True, idx, tool_name, refined_prompt
            # If the tool is not found, default to using the FrontalLobe
            return False, -1, 'FrontalLobe', user_input
        else:
            lobe_name = decision.get('lobe_name', 'FrontalLobe')
            refined_prompt = decision.get('refined_prompt', user_input)
            return False, -1, lobe_name, refined_prompt

    def process_input(self, user_input: str, reasoning: bool = True, sanitize: bool = True) -> str:
        """
        Process the input by deciding whether to use a tool or an LLM, utilizing advanced decision-making.
        """
        # Use advanced decision-making to determine the action
        use_tool, tool_index, lobe_or_tool_name, refined_prompt = self.determine_action(user_input, advanced=True)

        if use_tool:
            # Use the specified tool with the refined prompt
            return self.use_tool(refined_prompt, tool_index, sanitize=False)
        else:
            # Use the specified lobe (LLM) to generate a response
            lobe = self.brain.get_lobe_by_name(lobe_or_tool_name)
            if lobe is None:
                # Default to the FrontalLobe if the specified lobe is not found
                lobe = self.brain.get_lobe_by_name('FrontalLobe')

            # Pass the memory DataFrame directly
            memory = self.brain.memory.short_term_df
            response = lobe.process(user_input=refined_prompt, memory=memory)

            # Store the interaction in memory
            self.store_memory(user_input, response)

            return response

    def store_memory(self, user_input: str, response: str):
        """Store the user input and response in memory."""
        # Ensure the response is a string
        response_text = response if isinstance(response, str) else str(response)
        self.brain.memory.store_memory(user_input, response_text)

    # Add get_lobe_by_name method if not present in Brain class
    def get_lobe_by_name(self, lobe_name: str):
        """
        Retrieve a lobe instance by its class name.
        """
        return self.brain.get_lobe_by_name(lobe_name)

    def use_tool(self, user_input: str, tool_index: int, sanitize: bool = False) -> str:
        chosen_tool = self.toolkit.tools[tool_index]
        expression = user_input
        if self.verbose:
            print(f"Using tool '{chosen_tool.name}' with expression: '{expression}'")
        try:
            result = chosen_tool.invoke(expression)
        except Exception as e:
            result = f"An error occurred while using the tool '{chosen_tool.name}': {e}"
        return result

