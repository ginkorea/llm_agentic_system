from agents.brain.modules.module import Module


# PreFrontalCortex: Reflexive thinking and decision-making
class PreFrontalCortex(Module):
    """Responsible for reflexive thinking and quick decision-making, you act as the control center for the brain."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.7,
            memory_limit=3,
            system_message="You are responsible for reflexive thinking and quick decision-making, you act as the control center for the brain."
        )


# Frontal Module: Higher-level thinking and decision-making
class FrontalLobe(Module):
    """Handles higher-level thinking, complex reasoning, and decision-making."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.8,
            memory_limit=12,
            system_message="You are responsible for handling higher-level thinking, complex reasoning, and more rational decision-making."
        )


# Occipital Lobe: Pattern recognition and visual processing
class OccipitalLobe(Module):
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
class TemporalLobe(Module):
    """Responsible for language comprehension, memory recall, and auditory processing."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.5,
            memory_limit=7,
            system_message="You are responsible for language comprehension, memory recall, and auditory processing."
        )


# Parietal Lobe: Math and spatial reasoning
class ParietalLobe(Module):
    """Handles mathematical reasoning, spatial awareness, and problem-solving."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.2,
            memory_limit=5,
            system_message="You handle mathematical reasoning, spatial awareness, and problem-solving."
        )


# Cerebellum: Quick reflexive actions
class Cerebellum(Module):
    """Manages rapid reflexive actions with minimal reasoning."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.0,
            memory_limit=2,
            system_message="You manage rapid reflexive actions with minimal reasoning."
        )


# Broca’s Area: Conversational and structured speech
class BrocasArea(Module):
    """Focuses on generating structured speech, dialogue, and conversation."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.3,
            memory_limit=4,
            system_message="You focus on generating structured speech, dialogue, and conversation."
        )


# Amygdala: Sentiment analysis and emotional response
class Amygdala(Module):
    """Interprets and generates emotional responses."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.4,
            memory_limit=3,
            system_message="You focus on interpreting and generating emotional responses."
        )


# Cerebral Cortex: General problem-solving
class CerebralCortex(Module):
    """Handles general problem-solving and reasoning across various domains."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=10,
            system_message="You handle general problem-solving and reasoning across various domains."
        )
