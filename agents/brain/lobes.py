from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class Lobe:
    def __init__(self, model_name: str, temperature: float, memory_limit: int, system_message: str):
        """
        A base Lobe class that wraps a language model with a defined memory limit.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.memory_limit = memory_limit
        self.system_message = system_message
        self.model = ChatOpenAI(model=model_name, temperature=temperature)
        self.prompt_template = ChatPromptTemplate.from_messages([("system", self.system_message)])

    def get_info(self):
        """
        Returns a dictionary of the lobe's information.
        """
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "memory_limit": self.memory_limit,
            "system_message": self.system_message
        }

    def process(self, user_input: str, memory: list) -> str:
        """
        Process the input using the language model. It uses up to 'memory_limit' amount of the memory.
        """
        # Use only up to the defined memory limit
        recent_memory = memory[-self.memory_limit:]
        prompt = self.build_prompt(user_input, recent_memory)
        return self.model.run(prompt)

    def build_prompt(self, user_input: str, memory: list) -> str:
        """
        Build a full prompt, including system messages and memory using ChatPromptTemplate.
        """
        memory_context = "\n".join([f"User: {mem['user_input']}\nResponse: {mem['response']}" for mem in memory])
        return self.prompt_template.format(user_input=user_input, memory=memory_context)


# Prefrontal Cortex: Reflexive thinking and decision-making, mapped to GPT-3.5 Turbo
class PreFrontalCortex(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            memory_limit=3,
            system_message="You are responsible for reflexive thinking and quick decision-making."
        )

# Frontal Lobe: Higher-level thinking and decision-making, mapped to GPT-4
class FrontalLobe(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4",
            temperature=0.8,
            memory_limit=12,
            system_message="You are responsible for handling higher-level thinking, complex reasoning, and decision-making."
        )



# Occipital Lobe: Pattern recognition and visual processing, mapped to GPT-4 with Vision (or CLIP)
class OccipitalLobe(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4-vision",  # Assuming GPT-4 with Vision capabilities for visual tasks
            temperature=0.3,
            memory_limit=5,
            system_message="You process visual information and handle tasks related to pattern recognition."
        )


# Temporal Lobe: Language comprehension and memory recall, mapped to GPT-3.5 Turbo
class TemporalLobe(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-3.5-turbo",
            temperature=0.5,
            memory_limit=7,
            system_message="You are responsible for language comprehension, memory recall, and auditory processing."
        )


# Parietal Lobe: Math and spatial reasoning, mapped to Codex and math-focused models
class ParietalLobe(Lobe):
    def __init__(self):
        super().__init__(
            model_name="codex-davinci-002",  # Codex model for math and code
            temperature=0.2,
            memory_limit=5,
            system_message="You handle mathematical reasoning, spatial awareness, and problem-solving."
        )


# Cerebellum: Quick reflexive actions, mapped to lightweight models
class Cerebellum(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-3.5-turbo",
            temperature=0.0,
            memory_limit=2,
            system_message="You manage rapid reflexive actions with minimal reasoning."
        )


# Hippocampus: Memory recall and continuity, mapped to memory-augmented LLMs
class Hippocampus(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4",
            temperature=0.6,
            memory_limit=10,
            system_message="You are responsible for recalling long-term memory and maintaining continuity."
        )


# Broca’s Area: Conversational and structured speech, mapped to GPT-3.5 for dialogue tasks
class BrocasArea(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-3.5-turbo",
            temperature=0.3,
            memory_limit=4,
            system_message="You focus on generating structured speech, dialogue, and conversation."
        )


# Amygdala: Sentiment analysis and emotional response, mapped to sentiment analysis models
class Amygdala(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-3.5-turbo",  # Placeholder, could be a fine-tuned sentiment analysis model
            temperature=0.4,
            memory_limit=3,
            system_message="You focus on interpreting and generating emotional responses."
        )


# Cerebral Cortex: General problem-solving, mapped to general-purpose LLMs like GPT-4
class CerebralCortex(Lobe):
    def __init__(self):
        super().__init__(
            model_name="gpt-4",
            temperature=0.5,
            memory_limit=10,
            system_message="You handle general problem-solving and reasoning across various domains."
        )
