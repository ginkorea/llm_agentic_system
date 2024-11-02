from agents.brain.lobes.module import Module

# PreFrontalCortex: Reflexive thinking and decision-making
class PreFrontalCortex(Module):
    """Responsible for reflexive thinking and quick decision-making, acting as the control center for the brain."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",  # Supports system messages
            temperature=0.7,
            memory_limit=3,
            system_message="You are responsible for reflexive thinking and quick decision-making, acting as the control center for the brain."
        )

# FrontalLobe: Higher-level thinking and decision-making
class FrontalLobe(Module):
    """Handles higher-level thinking, complex reasoning, and decision-making."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",  # Supports system messages
            temperature=0.8,
            memory_limit=12,
            system_message="You handle higher-level thinking, complex reasoning, and decision-making."
        )

# OccipitalLobe: Pattern recognition and visual processing
class OccipitalLobe(Module):
    """Processes visual information and handles tasks related to pattern recognition."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",  # Supports image inputs and system messages
            temperature=0.3,
            memory_limit=5,
            system_message="You process visual information and handle tasks related to pattern recognition."
        )

# TemporalLobe: Language comprehension and memory recall
class TemporalLobe(Module):
    """Responsible for language comprehension, memory recall, and auditory processing."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",  # Supports system messages
            temperature=0.5,
            memory_limit=7,
            system_message="You handle language comprehension, memory recall, and auditory processing."
        )

# ParietalLobe: Math and spatial reasoning
class ParietalLobe(Module):
    """Handles mathematical reasoning, spatial awareness, and problem-solving."""

    def __init__(self):
        super().__init__(
            model_name="o1-mini",  # Advanced reasoning capabilities; system messages not supported
            temperature=0.2,
            memory_limit=5,
            system_message=None  # System message omitted due to lack of support
        )

# Cerebellum: Quick reflexive actions
class Cerebellum(Module):
    """Manages rapid reflexive actions with minimal reasoning."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",  # Supports system messages
            temperature=0.0,
            memory_limit=2,
            system_message="You manage rapid reflexive actions with minimal reasoning."
        )

# Broca’s Area: Conversational and structured speech
class BrocasArea(Module):
    """Focuses on generating structured speech, dialogue, and conversation."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",  # Supports system messages
            temperature=0.3,
            memory_limit=4,
            system_message="You focus on generating structured speech, dialogue, and conversation."
        )

# Amygdala: Sentiment analysis and emotional response
class Amygdala(Module):
    """Interprets and generates emotional responses."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",  # Supports system messages
            temperature=0.4,
            memory_limit=3,
            system_message="You interpret and generate emotional responses."
        )

# CerebralCortex: General problem-solving
class CerebralCortex(Module):
    """Handles general problem-solving and reasoning across various domains."""

    def __init__(self):
        super().__init__(
            model_name="o1-preview",  # Advanced reasoning capabilities; system messages not supported
            temperature=1,
            memory_limit=10,
            system_message=None  # System message omitted due to lack of support
        )


# Test the CerbralCortex module

if __name__ == "__main__":
    from const.sk import kc

    module = CerebralCortex()
    print(module.get_info())
    print(module.process(["What is the capital of France?"]))
    print(module.build_prompt_messages("What is the capital of France?", []))
    module.print_model_info()