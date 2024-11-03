# core.py
from typing import Tuple, Any

from pandas import DataFrame

from agents.brain.prompts.examples.base_examples import ExamplesBase as BaseExamples
from agents.brain.lobes.simple_modules import ControlModule, MainModule, MemoryModule
import json


class Brain:
    def __init__(self, toolkit, forget_threshold: int = 10, verbose: bool = True, memory_type='embedded', include_routing_module: bool = False):
        self.verbose = verbose
        self.include_routing_module = include_routing_module
        self.milestone = {}
        self.goal = None  # Define overarching goal for chaining mode

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

        # Set the first module as the router for prompt handling
        self.router = self.modules[0]
        self.previous_output = False

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

    def initialize_prompt_builders(self):
        """
        Initialize the prompt builders for all modules.
        This method should be called after tool and module descriptions are generated.
        """
        for module in self.modules:
            module.build_prompt_builder(
                brain=self
            )

    def determine_action(self, user_input: str, previous_output: bool = False) -> dict:
        """
        Use the router to determine if the input should be handled by a tool or a module.
        """
        # Generate prompt using router's StructuredPrompt
        try:
            prompt = self.router.prompt_builder.build_prompt(user_input, previous_output)
        except AttributeError:
            self.initialize_prompt_builders()
            print("Prompt builders initialized.")
            print("Re-running prompt generation.")
            print(f"Router: {self.router}")
            prompt = self.router.prompt_builder.build_prompt(user_input, previous_output)
        if self.verbose: print(f"Constructed prompt: {prompt}")

        # Retrieve short-term memory as context
        short_term_memory = self.memory.recall_memory(0, self.memory.short_term_length).to_dict('records')
        prompt_messages = self.router.build_memory_context(user_input=prompt, memory=short_term_memory)

        # Process prompt to obtain decision
        decision_response = self.router.process(prompt_messages)

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

    def process_input(self, prompt_input: str, chaining_mode: bool = False) -> tuple[str | DataFrame, Any] | str:
        """
        Process the input by deciding whether to use a tool or a module, with a formatted memory context.
        """
        if chaining_mode:
            if not self.check_goal_achieved():
                action = self.determine_action(prompt_input, previous_output=self.previous_output)
                self.previous_output = True
                return self.execute_action(action)
            else:
                return "Goal achieved."
        return self.execute_action(self.determine_action(prompt_input))

    def execute_action(self, action):
        """
        Execute the given action based on the use_tool flag and return the result.
        Avoid double-logging in chaining mode.
        """
        if action["use_tool"]:
            result, using = self.use_tool(action["refined_prompt"], action["tool_index"]), action["tool_name"]
            if self.verbose: print(f"Using tool '{using}' to process the input.")

        else:
            selected_module = self.modules[action["module_index"]]
            result, using = selected_module.process(action["refined_prompt"]), selected_module.__class__.__name__
            if self.verbose: print(f"Using module '{using}' to process the input.")
        print(f"Result: {result}")
        print(f"Using: {using}")
        print(action["refined_prompt"])
        self.store_memory(action["refined_prompt"], result, module=using)

        return result, using

    def check_goal_achieved(self):
        # Placeholder for goal-checking logic
        return False

    def store_memory(self, user_input: str, response: str, module: str = ""):
        """Store the user input, response, and module/tool name in memory only if not already stored."""
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
