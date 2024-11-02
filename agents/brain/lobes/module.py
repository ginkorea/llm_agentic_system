from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from typing import List, Dict, Optional


class Module:
    """Base class representing a lobe or module of the brain that interfaces with language models.

    This class provides a structure for defining lobes that can utilize different LLMs
    and manage their configurations, such as model name, temperature, and memory limits.
    It can be customized to integrate specific functionalities as needed.
    """

    def __init__(self, model_name: str = None, temperature: float = None, memory_limit: int = 10,
                 system_message: Optional[str] = None, initialize_model: bool = True, alt_system_message: Optional[str] = None):
        self.model_name = model_name
        self.temperature = temperature
        self.memory_limit = memory_limit
        self.system_message = system_message
        self.alt_system_message = alt_system_message

        # Initialize the language model if the parameters are provided
        if initialize_model and self.model_name and self.temperature is not None:
            self.model = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)
        else:
            self.model = None  # No model is required for lobes like Hippocampus

    def get_info(self):
        """Returns configuration information about the lobe."""
        system_message = self.system_message if self.system_message else self.alt_system_message
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "memory_limit": self.memory_limit,
            "system_message": system_message
        }

    def process(self, prompt_messages: List[Dict[str, str]]) -> str:
        """
        Process user input using the configured language model with a prompt message format.
        """
        response = self.model.invoke(prompt_messages)  # Pass prompt directly
        return response.content.strip()

    def build_prompt_messages(self, user_input: str, memory: list):
        """Construct the prompt messages for the language model using system and user messages.

        This includes the system message, past user inputs, and the current user input.
        """
        messages = []

        # Add system message only if it is not None
        if self.system_message is not None:
            messages.append(SystemMessage(content=self.system_message))

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
