import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

class Module:
    """Base class representing a lobe or module of the brain that interfaces with language models.

    This class provides a structure for defining lobes that can utilize different LLMs
    and manage their configurations, such as model name, temperature, and memory limits.
    It can be customized to integrate specific functionalities as needed.
    """

    def __init__(self, model_name: str = None, temperature: float = None, memory_limit: int = 10,
                 system_message: str = "", initialize_model: bool = True):
        self.model_name = model_name
        self.temperature = temperature
        self.memory_limit = memory_limit
        self.system_message = system_message

        # Initialize the language model if the parameters are provided
        if initialize_model and self.model_name and self.temperature is not None:
            self.model = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)
        else:
            self.model = None  # No model is required for lobes like Hippocampus

    def get_info(self):
        """Returns configuration information about the lobe."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "memory_limit": self.memory_limit,
            "system_message": self.system_message
        }

    def process(self, user_input: str, memory) -> str:
        """Process user input using the configured language model.

        This method retrieves relevant memory based on the type (DataFrame or list),
        constructs a prompt from recent memories, and invokes the model to get a response.
        """
        # Handle memory based on its type
        if isinstance(memory, pd.DataFrame):
            # Check if DataFrame is empty
            if not memory.empty:
                memory_list = memory.to_dict('records')
                recent_memory = memory_list[-self.memory_limit:]  # Fetch recent memories
            else:
                recent_memory = []
        elif isinstance(memory, list):
            recent_memory = memory[-self.memory_limit:] if memory else []
        else:
            # If memory is None or unrecognized type
            recent_memory = []

        messages = self.build_prompt_messages(user_input, recent_memory)
        response = self.model.invoke(messages)  # Invoke the LLM to get a response
        return response.content.strip()

    def build_prompt_messages(self, user_input: str, memory: list):
        """Construct the prompt messages for the language model using system and user messages.

        This includes the system message, past user inputs, and the current user input.
        """
        messages = [SystemMessage(content=self.system_message)]
        for mem in memory:
            messages.append(HumanMessage(content=mem['user_input']))  # Previous user input
            messages.append(AIMessage(content=mem['response']))  # Corresponding AI response
        messages.append(HumanMessage(content=user_input))  # Current user input
        return messages

    def print_model_info(self):
        """Prints information about the model and its configuration."""
        print(f"Model: {self.model_name}")
        print(f"Temperature: {self.temperature}")
        print(f"Memory Limit: {self.memory_limit}")
        print(f"System Message: {self.system_message}")

