from agents.brain.lobes.lobes import (PreFrontalCortex, FrontalLobe)
from agents.brain.lobes.hippocampus import Hippocampus


class ControlModule(PreFrontalCortex):

    """
    ControlModule: Responsible for reflexive thinking and quick decision-making, you act as the control center for the brain. Uses GPT-4o-mini.
    """

    def __init__(self):
        super().__init__()


class MainModule(FrontalLobe):

    """
    MainModule: Handles higher-level thinking, complex reasoning, and decision-making, used when a more rational decision is needed.  Uses GPT-4o.
    """

    def __init__(self):
        super().__init__()


class MemoryModule(Hippocampus):

    """
    MemoryModule: Responsible for storing and recalling memories, you act as the brain's memory center. Uses Jina AI for memory storage and retrieval.
    """

    def __init__(self, brain):
        super().__init__(brain=brain)