# agents/brain/lobes.py

import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


class Lobe:
    def __init__(self, model_name: str = None, temperature: float = None, memory_limit: int = 10,
                 system_message: str = "", initialize_model: bool = True):
        self.model_name = model_name
        self.temperature = temperature
        self.memory_limit = memory_limit
        self.system_message = system_message

        if initialize_model and self.model_name and self.temperature is not None:
            self.model = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)
        else:
            self.model = None  # No model is required for lobes like Hippocampus

    def get_info(self):
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "memory_limit": self.memory_limit,
            "system_message": self.system_message
        }

    def process(self, user_input: str, memory) -> str:
        """
        Process the input using the language model.
        """
        # Handle memory based on its type
        if isinstance(memory, pd.DataFrame):
            # Check if DataFrame is empty
            if not memory.empty:
                memory_list = memory.to_dict('records')
                recent_memory = memory_list[-self.memory_limit:]
            else:
                recent_memory = []
        elif isinstance(memory, list):
            recent_memory = memory[-self.memory_limit:] if memory else []
        else:
            # If memory is None or unrecognized type
            recent_memory = []

        messages = self.build_prompt_messages(user_input, recent_memory)
        response = self.model.invoke(messages)
        return response.content.strip()

    def build_prompt_messages(self, user_input: str, memory: list):
        messages = []
        messages.append(SystemMessage(content=self.system_message))
        for mem in memory:
            messages.append(HumanMessage(content=mem['user_input']))
            messages.append(AIMessage(content=mem['response']))
        messages.append(HumanMessage(content=user_input))
        return messages

    def print_model_info(self):
        print(f"Model: {self.model_name}")
        print(f"Temperature: {self.temperature}")
        print(f"Memory Limit: {self.memory_limit}")
        print(f"System Message: {self.system_message}")

# PreFrontalCortex: Reflexive thinking and decision-making
class PreFrontalCortex(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.7,
            memory_limit=3,
            system_message="You are responsible for reflexive thinking and quick decision-making."
        )

# Frontal Lobe: Higher-level thinking and decision-making
class FrontalLobe(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.8,
            memory_limit=12,
            system_message="You are responsible for handling higher-level thinking, complex reasoning, and decision-making."
        )

# Occipital Lobe: Pattern recognition and visual processing
class OccipitalLobe(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4o",  # GPT-4o supports image inputs
            temperature=0.3,
            memory_limit=5,
            system_message="You process visual information and handle tasks related to pattern recognition."
        )

# Temporal Lobe: Language comprehension and memory recall
class TemporalLobe(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.5,
            memory_limit=7,
            system_message="You are responsible for language comprehension, memory recall, and auditory processing."
        )

# Parietal Lobe: Math and spatial reasoning
class ParietalLobe(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.2,
            memory_limit=5,
            system_message="You handle mathematical reasoning, spatial awareness, and problem-solving."
        )

# Cerebellum: Quick reflexive actions
class Cerebellum(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.0,
            memory_limit=2,
            system_message="You manage rapid reflexive actions with minimal reasoning."
        )



# Broca’s Area: Conversational and structured speech
class BrocasArea(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.3,
            memory_limit=4,
            system_message="You focus on generating structured speech, dialogue, and conversation."
        )

# Amygdala: Sentiment analysis and emotional response
class Amygdala(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.4,
            memory_limit=3,
            system_message="You focus on interpreting and generating emotional responses."
        )

# Cerebral Cortex: General problem-solving
class CerebralCortex(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=10,
            system_message="You handle general problem-solving and reasoning across various domains."
        )
