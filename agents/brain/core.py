# agents/brain/core.py
from .build_prompt import default_prompt_builder
from .examples import prompt_examples
from .lobes import (
    PreFrontalCortex, OccipitalLobe, FrontalLobe, TemporalLobe, ParietalLobe,
    Cerebellum, BrocasArea, Amygdala, CerebralCortex
)
from .hippocampus import Hippocampus
import json


class Brain:
    def __init__(self, toolkit, forget_threshold: int = 10, verbose: bool = True, memory_type='embedded'):

        # Set the verbose flag
        self.verbose = verbose

        # Initialize memory based on the memory_type parameter
        if memory_type == 'cuda':
            from .memory.cuda_embedded import CudaMemoryWithEmbeddings
            self.memory = CudaMemoryWithEmbeddings(forget_threshold=forget_threshold)
        elif memory_type == 'openvino':
            from .memory.ov_embedded import OpenvinoMemoryWithEmbeddings
            self.memory = OpenvinoMemoryWithEmbeddings(forget_threshold=forget_threshold)
        elif memory_type == 'embedded':
            from .memory.embedded import EmbeddedMemory
            self.memory = EmbeddedMemory(forget_threshold=forget_threshold)
        else:
            from .memory.simple import SimpleMemory
            self.memory = SimpleMemory(forget_threshold=forget_threshold)

        self.toolkit = toolkit  # Add toolkit to Brain

        # Initialize lobes using the specialized classes
        self.lobes = [
            PreFrontalCortex(),
            FrontalLobe(),
            OccipitalLobe(),
            TemporalLobe(),
            ParietalLobe(),
            Cerebellum(),
            BrocasArea(),
            Amygdala(),
            CerebralCortex(),
            Hippocampus(self)
        ]

    def get_lobe_info(self):
        """
        Dynamically generates a list of available lobes and their descriptions.
        """
        lobe_info = {}
        for idx, lobe in enumerate(self.lobes):
            lobe_info[idx] = {
                'name': lobe.__class__.__name__,
                'description': lobe.system_message  # Assuming each lobe has a system_message attribute
            }
        return lobe_info

    def get_tool_info(self):
        """
        Generates a dictionary of available tools and their descriptions.
        """
        tool_info = {tool.name: tool.description for tool in self.toolkit.tools}
        return tool_info

    def determine_action(self, user_input: str) -> dict:
        """
        Use the PreFrontalCortex to determine if the input should be handled by a tool or a lobe.

        Returns:
            - Dictionary containing action information.
        """
        # Get tool and lobe information
        tool_info = self.get_tool_info()
        lobe_info = self.get_lobe_info()

        # Build tool descriptions
        tool_descriptions = "\n".join([f"{name}: {desc}" for name, desc in tool_info.items()])

        # Build lobe descriptions
        lobe_descriptions = "\n".join(
            [f"{idx}: {info['name']} - {info['description']}" for idx, info in lobe_info.items()]
        )

        # Build examples
        examples = prompt_examples

        # Construct the prompt for the PreFrontalCortex to make a decision
        prompt = default_prompt_builder(tool_descriptions=tool_descriptions, lobe_descriptions=lobe_descriptions,
                                        examples=examples, user_input=user_input)

        # The PreFrontalCortex determines which action to take
        prefrontal_cortex = self.lobes[0]  # Assuming PreFrontalCortex is at index 0
        decision_response = prefrontal_cortex.process(user_input=prompt, memory=self.memory.short_term_df)

        # Parse the JSON response
        try:
            decision = json.loads(decision_response)
            use_tool = decision.get('use_tool', False)
            refined_prompt = decision.get('refined_prompt', user_input)

            if use_tool:
                tool_name = decision.get('tool_name')
                # Find the tool index based on the tool name
                tool_index = next((idx for idx, tool in enumerate(self.toolkit.tools) if tool.name == tool_name), None)
                if tool_index is not None:
                    return {
                        "use_tool": True,
                        "tool_index": tool_index,
                        "tool_name": tool_name,
                        "refined_prompt": refined_prompt
                    }
            else:
                lobe_index = int(decision.get('lobe_index', 0))
                return {
                    "use_tool": False,
                    "lobe_index": lobe_index,
                    "lobe_name": self.lobes[lobe_index].__class__.__name__,
                    "refined_prompt": refined_prompt
                }
        except (json.JSONDecodeError, KeyError, ValueError):
            # If parsing fails, default to using the FrontalLobe
            return {
                "use_tool": False,
                "lobe_index": 1,  # FrontalLobe
                "lobe_name": "FrontalLobe",
                "refined_prompt": user_input
            }

    def process_input(self, user_input: str) -> str:
        """
        Process the input by deciding whether to use a tool or a lobe.
        """
        action = self.determine_action(user_input)
        if action["use_tool"]:
            # Use the specified tool with the refined prompt
            result = self.use_tool(action["refined_prompt"], action["tool_index"])
        else:
            # Use the specified lobe to generate a response
            selected_lobe = self.lobes[action["lobe_index"]]
            if self.verbose:
                print(f"Using lobe '{selected_lobe.__class__.__name__}' to process the input.")
            result = selected_lobe.process(user_input=action["refined_prompt"], memory=self.memory.short_term_df)

        # Store the interaction in memory
        self.store_memory(user_input, result)

        return result

    def store_memory(self, user_input: str, response: str):
        """Store the user input and response in memory."""
        self.memory.store_memory('user_input: '+ str(user_input),'response: ' + str(response))

    def get_lobe_by_name(self, lobe_name: str):
        """
        Retrieve a lobe instance by its class name.
        """
        for lobe in self.lobes:
            if lobe.__class__.__name__ == lobe_name:
                return lobe
        return None

    def use_tool(self, user_input: str, tool_index: int) -> str:
        chosen_tool = self.toolkit.tools[tool_index]
        try:
            if chosen_tool.name == 'search':
                # You may need to parse the user_input to extract the query and n_sites
                query = user_input
                n_sites = 5  # Set default or parse from user_input
                expression = {'query_parameters': {'query': query, 'n_sites': n_sites}}
            else:
                expression = user_input

            if self.verbose:
                print(f"Using tool '{chosen_tool.name}' with expression: '{expression}'")

            result = chosen_tool.invoke(expression)
        except Exception as e:
            result = f"An error occurred while using the tool '{chosen_tool.name}': {e}"
        return result

