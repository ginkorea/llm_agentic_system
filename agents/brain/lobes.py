import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


class Lobe:
    """Base class representing a lobe of the brain that interfaces with language models.

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


# PreFrontalCortex: Reflexive thinking and decision-making
class PreFrontalCortex(Lobe):
    """Responsible for reflexive thinking and quick decision-making, you act as the control center for the brain."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.7,
            memory_limit=3,
            system_message="You are responsible for reflexive thinking and quick decision-making, you act as the control center for the brain."
        )


# Frontal Lobe: Higher-level thinking and decision-making
class FrontalLobe(Lobe):
    """Handles higher-level thinking, complex reasoning, and decision-making."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.8,
            memory_limit=12,
            system_message="You are responsible for handling higher-level thinking, complex reasoning, and more rational decision-making."
        )


# Occipital Lobe: Pattern recognition and visual processing
class OccipitalLobe(Lobe):
    """Processes visual information and handles tasks related to pattern recognition."""
    #TODO: Add image processing capabilities

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",  # GPT-4o supports image inputs
            temperature=0.3,
            memory_limit=5,
            system_message="You process visual information and handle tasks related to pattern recognition."
        )


# Temporal Lobe: Language comprehension and memory recall
class TemporalLobe(Lobe):
    """Responsible for language comprehension, memory recall, and auditory processing."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.5,
            memory_limit=7,
            system_message="You are responsible for language comprehension, memory recall, and auditory processing."
        )


# Parietal Lobe: Math and spatial reasoning
class ParietalLobe(Lobe):
    """Handles mathematical reasoning, spatial awareness, and problem-solving."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.2,
            memory_limit=5,
            system_message="You handle mathematical reasoning, spatial awareness, and problem-solving."
        )


# Cerebellum: Quick reflexive actions
class Cerebellum(Lobe):
    """Manages rapid reflexive actions with minimal reasoning."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.0,
            memory_limit=2,
            system_message="You manage rapid reflexive actions with minimal reasoning."
        )


# Broca’s Area: Conversational and structured speech
class BrocasArea(Lobe):
    """Focuses on generating structured speech, dialogue, and conversation."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.3,
            memory_limit=4,
            system_message="You focus on generating structured speech, dialogue, and conversation."
        )


# Amygdala: Sentiment analysis and emotional response
class Amygdala(Lobe):
    """Interprets and generates emotional responses."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.4,
            memory_limit=3,
            system_message="You focus on interpreting and generating emotional responses."
        )


# Cerebral Cortex: General problem-solving
class CerebralCortex(Lobe):
    """Handles general problem-solving and reasoning across various domains."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=10,
            system_message="You handle general problem-solving and reasoning across various domains."
        )
