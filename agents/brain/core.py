# core.py

from agents.brain.prompts.build_prompt import default_prompt_builder
from agents.brain.prompts.examples import ExamplesBase as BaseExamples
from agents.brain.lobes.simple_modules import ControlModule, MainModule, MemoryModule
import json


class Brain:
    def __init__(self, toolkit, forget_threshold: int = 10, verbose: bool = True, memory_type='embedded', include_routing_module: bool = False):
        self.verbose = verbose
        self.include_routing_module = include_routing_module
        self.milestone = {}

        # Initialize memory based on the memory_type parameter
        self.memory = None
        self.initialize_memory(memory_type, forget_threshold)

        # Initialize toolkit and modules
        self.toolkit = toolkit
        self.modules = self.load_modules()

        # Pre-generate tool and module descriptions
        self.tool_descriptions = self.build_tool_descriptions()
        self.module_descriptions = self.build_module_descriptions(include_routing_module)
        self.examples = BaseExamples()

    def initialize_memory(self, memory_type, forget_threshold):
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

    def load_modules(self):
        return [
            ControlModule(),
            MainModule(),
            MemoryModule(brain=self)
        ]

    def build_tool_descriptions(self) -> str:
        tool_info = {tool.name: tool.description for tool in self.toolkit.tools}
        if self.verbose: print(f"Tool information initialized: {tool_info}")
        return "\n".join([f"{name}: {desc}" for name, desc in tool_info.items()])

    def build_module_descriptions(self, include_routing_module: bool) -> str:
        module_info = {}
        start_index = 0 if include_routing_module else 1
        for idx, module in enumerate(self.modules[start_index:], start=start_index):
            sys_msg = module.system_message or module.alt_system_message or "No system message available."
            module_info[idx] = {
                'name': module.__class__.__name__,
                'description': sys_msg
            }
        if self.verbose: print(f"Module information initialized: {module_info}")
        return "\n".join([f"{idx}: {info['name']} - {info['description']}" for idx, info in module_info.items()])

    def determine_action(self, user_input: str) -> dict:
        """
        Use the routing module to determine if the input should be handled by a tool or a module.
        """
        # Generate prompt
        prompt = default_prompt_builder(
            tool_descriptions=self.tool_descriptions,
            module_descriptions=self.module_descriptions,
            examples=self.examples.get_examples(),
            user_input=user_input
        )
        if self.verbose: print(f"Constructed prompt: {prompt}")

        router = self.modules[0]
        short_term_memory = self.memory.recall_memory(0, self.memory.short_term_length).to_dict('records')
        prompt_messages = router.build_prompt_messages(user_input=prompt, memory=short_term_memory)
        decision_response = router.process(prompt_messages)

        # Process the decision in JSON format
        try:
            decision = json.loads(decision_response)
            use_tool = decision.get('use_tool', False)
            refined_prompt = decision.get('refined_prompt', user_input)

            if use_tool:
                tool_name = decision.get('tool_name')
                tool_index = next((idx for idx, tool in enumerate(self.toolkit.tools) if tool.name == tool_name), None)
                if tool_index is not None:
                    return {
                        "use_tool": True,
                        "tool_index": tool_index,
                        "tool_name": tool_name,
                        "refined_prompt": refined_prompt
                    }
            else:
                module_index = int(decision.get('module_index', 1 if not self.include_routing_module else 0))
                return {
                    "use_tool": False,
                    "module_index": module_index,
                    "module_name": self.modules[module_index].__class__.__name__,
                    "refined_prompt": refined_prompt
                }
        except (json.JSONDecodeError, KeyError, ValueError):
            return {
                "use_tool": False,
                "module_index": 1,
                "module_name": "MainModule",
                "refined_prompt": user_input
            }


    def process_input(self, user_input: str) -> str:
        """
        Process the input by deciding whether to use a tool or a module, with a formatted memory context.
        """
        action = self.determine_action(user_input)
        formatted_memory = self.memory.format_memory()  # Get formatted memory context

        if action["use_tool"]:
            result = self.use_tool(action["refined_prompt"], action["tool_index"])
            # Store tool response in memory with tool name
            self.store_memory(user_input, result, module=action["tool_name"])
        else:
            selected_module = self.modules[action["module_index"]]
            if self.verbose:
                print(f"Using module '{selected_module.__class__.__name__}' to process the input.")

            # Set short-term memory length dynamically
            self.memory.set_short_term_length(selected_module.memory_limit)

            # Prepare prompt with formatted memory context
            prompt_messages = [{"role": "system", "content": selected_module.system_message}] + formatted_memory
            prompt_messages.append({"role": "user", "content": action["refined_prompt"]})

            # Send prompt to model and get response
            result = selected_module.process(prompt_messages)

            # Store module response in memory with module name
            self.store_memory(user_input, result, module=selected_module.__class__.__name__)

        return result

    def store_memory(self, user_input: str, response: str, module: str = ""):
        """Store the user input, response, and module/tool name in memory."""
        self.memory.store_memory(user_input, response, module=module)

    def get_module_by_name(self, module_name: str, include_routing_module: bool = False):
        """
        Retrieve a module instance by its class name, with the option to include the routing module.
        """
        start_index = 0 if include_routing_module else 1
        for module in self.modules[start_index:]:
            if module.__class__.__name__ == module_name:
                return module
        return None

    def use_tool(self, user_input: str, tool_index: int) -> str:
        chosen_tool = self.toolkit.tools[tool_index]
        try:
            if chosen_tool.name == 'search':
                # Parse user_input to extract the query and n_sites if needed
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
