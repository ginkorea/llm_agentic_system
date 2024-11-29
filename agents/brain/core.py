# core.py

from pandas import DataFrame
from agents.brain.lobes.simple_modules import ControlModule, MainModule, MemoryModule
from agents.brain.prompts.examples import ExamplesBase
import json
import logging


class Brain:
    def __init__(self, toolkit, forget_threshold=10, verbose=True, memory_type='embedded', include_routing_module=False, goal=None, goal_file=None, work_folder="workbench"):
        """
        Initializes the Brain with memory, tools, and modules.

        Parameters:
        - toolkit: Collection of tools available for the Brain.
        - forget_threshold: Threshold for memory forgetting.
        - verbose: If True, prints debugging information.
        - memory_type: Type of memory to initialize.
        - include_routing_module: Whether to include a routing module.
        - goal: The main goal object for the Brain.
        - goal_file: File for goal-related information, if applicable.
        """
        self.logger = logging.getLogger(self.__class__.__name__)  # Logger specific to Brain
        self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        self.verbose = verbose
        self.include_routing_module = include_routing_module
        self.memory = None
        self.initialize_memory(memory_type, forget_threshold)
        self.toolkit = toolkit
        self.modules = self.load_modules()
        self.tool_descriptions = self.build_tool_descriptions()
        self.module_descriptions = self.build_module_descriptions(include_routing_module)
        self.examples = ExamplesBase()
        self.router = self.modules[0]  # Set the first module as the router
        self.previous_output = False
        self.goal = goal
        self.goal_file = goal_file
        self.knowledge_base = {}
        self.work_folder = work_folder # Folder for storing work files

    def judge_output(self, output: str) -> tuple[bool, str]:
        """
        Evaluates if the current output meets the current milestone's criteria.

        Parameters:
        - output: The output to evaluate.

        Returns:
        - True if the milestone is achieved, otherwise False.
        """
        # ANSI escape codes for color
        green = "\033[92m"  # Green text
        red = "\033[91m"  # Red text
        reset = "\033[0m"  # Reset text color to default

        current_milestone = self.goal.current_milestone()
        judge = current_milestone.description + "Judge"
        if current_milestone:
            is_achieved, judge_output = current_milestone.is_achieved(self, output)
            self.memory.store_memory(output, judge_output, module=judge)
            if is_achieved:
                print(f"{green}Milestone '{current_milestone.description}' achieved.{reset}")
                self.goal.update_progress()
            else:
                print(f"{red}Milestone '{current_milestone.description}' not achieved.{reset}")
            return is_achieved, judge_output
        return False, ""

    def initialize_memory(self, memory_type, forget_threshold):
        """
        Initializes the memory based on the memory type specified.

        Parameters:
        - memory_type: Type of memory to use.
        - forget_threshold: Threshold for memory forgetting.
        """
        if memory_type == 'cuda':
            from .memory.cuda_embedded import CudaMemoryWithEmbeddings
            self.memory = CudaMemoryWithEmbeddings(forget_threshold=forget_threshold)
        elif memory_type == 'openvino':
            from .memory.ov_embedded import OpenvinoMemoryWithEmbeddings
            self.memory = OpenvinoMemoryWithEmbeddings(forget_threshold=forget_threshold)
        elif memory_type == 'embedded':
            from .memory.embedded import EmbeddedMemory
            self.memory = EmbeddedMemory()
        else:
            from .memory.simple import SimpleMemory
            self.memory = SimpleMemory()

    def load_modules(self):
        """
        Loads the default modules for the Brain.

        Returns:
        - A list of module instances.
        """
        try:
            return [
                ControlModule(),
                MainModule(),
                MemoryModule(brain=self)
            ]
        except Exception as e:
            if self.verbose:
                print(f"Error loading modules: {e}")
            return []

    def build_tool_descriptions(self) -> str:
        """
        Builds descriptions for all tools in the toolkit.

        Returns:
        - A formatted string with tool descriptions.
        """
        tool_info = {tool.name: tool.description for tool in self.toolkit.tools}
        if self.verbose: print(f"Tool information initialized: {tool_info}")
        return "\n".join([f"{name}: {desc}" for name, desc in tool_info.items()])

    def build_module_descriptions(self, include_routing_module: bool) -> str:
        """
        Builds descriptions for all modules.

        Parameters:
        - include_routing_module: Whether to include the routing module in descriptions.

        Returns:
        - A formatted string with module descriptions.
        """
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
        Initializes prompt builders for all modules.
        Should be called after generating tool and module descriptions.
        """
        for module in self.modules:
            module.build_prompt_builder(brain=self)

    def add_memory_context(self, prompt: str, module=None) -> list:
        """
        Retrieves and formats the memory context for a given module or router.

        Parameters:
        - prompt: The current prompt for which memory context is needed.
        - module: The module for which to build memory context. If None, defaults to the router.

        Returns:
        - A formatted list of memory entries for use in structured prompts.
        """
        if self.memory.long_term_df.empty:
            if self.verbose:
                print("No memory available in long_term_df.")
            return []

        # Retrieve the most recent short-term memories
        start = max(0, len(self.memory.long_term_df) - self.memory.short_term_length)
        short_term_memory = self.memory.recall_memory(start, len(self.memory.long_term_df), long_term=True).to_dict(
            'records')

        if self.verbose:
            print(f"Short-term memory retrieved: {short_term_memory}")

        # Use the provided module or default to the router to build memory context
        target_module = module if module else self.router
        memory_context = target_module.build_memory_context(user_input=prompt, memory=short_term_memory)

        if self.verbose:
            print(f"Formatted memory context for {target_module.__class__.__name__}: {memory_context}")

        return memory_context

    def encode_json(self, decision_response: str, user_input: str) -> dict:
        """
        Parses the JSON response from the decision process and extracts relevant information.

        Parameters:
        - decision_response: The JSON string response from the router.
        - user_input: The original input from the user, used as a fallback.

        Returns:
        - A structured dictionary indicating whether to use a tool or module, along with indices and prompts.
        """
        try:
            decision = json.loads(decision_response)
            use_tool = decision.get('use_tool', False)
            refined_prompt = decision.get('refined_prompt', user_input)

            if use_tool:
                tool_name = decision.get('tool_name')
                tool_index = next((idx for idx, tool in enumerate(self.toolkit.tools) if tool.name == tool_name), None)
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
            # Default to MainModule if parsing fails
            return {
                "use_tool": False,
                "module_index": 1,
                "module_name": "MainModule",
                "refined_prompt": user_input
            }

    def determine_action(self, user_input: str, previous_output: bool = False) -> dict:
        """
        Determines if the input should be handled by a tool or a module.

        Parameters:
        - user_input: The input from the user or task.
        - previous_output: If True, incorporates previous module's output for chaining.

        Returns:
        - A structured dictionary indicating the action to take.
        """

        try:
            prompt = self.router.prompt_builder.build_prompt(user_input, previous_output)
        except AttributeError:
            self.initialize_prompt_builders()
            if self.verbose:
                print("Re-running prompt generation.")
            prompt = self.router.prompt_builder.build_prompt(user_input, previous_output)

        if self.verbose:
            print(f"Constructed prompt: {prompt}")

        # Process the input and return the action to take
        self.memory.short_term_length = self.router.memory_limit # Set the memory limit for the current module
        prompt_messages = self.add_memory_context(prompt) # Add memory context to the prompt
        decision_response = self.router.process(prompt_messages) # Process the prompt with the router
        return_json = self.encode_json(decision_response, user_input) # Parse the JSON response
        self.memory.store_memory(user_input, return_json, module="Router") # Store the decision in memory
        return return_json

    def process_input(self, prompt_input: str, chaining_mode: bool = False) -> tuple[str | DataFrame, str, bool, str]:
        """
        Processes the input by deciding whether to use a tool or module and evaluates milestone completion.

        Parameters:
        - prompt_input: The input prompt to process.
        - chaining_mode: If True, checks milestone completion in chaining mode.

        Returns:
        - The result of executing the action and the module/tool used.
        """
        result, using = self.execute_action(self.determine_action(prompt_input))
        if chaining_mode and self.goal and not self.goal.is_complete():
            achieved, judge_output = self.judge_output(result)
        else:
            achieved, judge_output = False, ""
        return result, judge_output, achieved, using

    def execute_action(self, action):
        """
        Executes the given action based on whether a tool or module is selected.

        Parameters:
        - action: The structured dictionary with details about the action to execute.

        Returns:
        - The result of the action and the name of the module/tool used.
        """
        refined_prompt = action["refined_prompt"]
        if action["use_tool"]:
            result = self.use_tool(refined_prompt, action["tool_index"])
        else:
            selected_module = self.modules[action["module_index"]]
            self.memory.short_term_length = selected_module.memory_limit
            prompt_with_memory_context = self.add_memory_context(refined_prompt, module=selected_module)
            result = selected_module.process(prompt_with_memory_context)
            self.store_memory(refined_prompt, result, module=action.get("module_name", "Unknown Module"))
        return result, action.get("module_name", "Unknown Module")

    def store_memory(self, user_input: str, response: str, module: str = ""):
        """
        Stores the user input, response, and module/tool name in memory.

        Parameters:
        - user_input: The original input from the user.
        - response: The output response to store.
        - module: The name of the module/tool used.
        """
        self.memory.store_memory(user_input, response, module=module)

    def get_module_by_name(self, module_name: str, include_routing_module: bool = False):
        """
        Retrieves a module instance by its class name.

        Parameters:
        - module_name: Name of the module to retrieve.
        - include_routing_module: Whether to include the routing module.

        Returns:
        - The module instance if found, otherwise None.
        """
        start_index = 0 if include_routing_module else 1
        for module in self.modules[start_index:]:
            if module.__class__.__name__ == module_name:
                return module
        return None

    def use_tool(self, user_input: str, tool_index: int) -> str:
        """
        Uses the specified tool with the given input.

        Parameters:
        - user_input: The input to provide to the tool.
        - tool_index: Index of the tool to use.

        Returns:
        - The result from using the tool.
        """
        chosen_tool = self.toolkit.tools[tool_index]
        try:
            if chosen_tool.name == 'search':
                query = user_input
                n_sites = 5  # Default number of sites to search
                expression = {'query_parameters': {'query': query, 'n_sites': n_sites}}
            else:
                expression = user_input

            if self.verbose:
                print(f"Using tool '{chosen_tool.name}' with expression: '{expression}'")

            result = chosen_tool.invoke(expression)
        except Exception as e:
            result = f"An error occurred while using the tool '{chosen_tool.name}': {e}"
        return result

