from agents.brain.core import Brain
from agents.brain.modules.lobes import (
    PreFrontalCortex, OccipitalLobe, FrontalLobe, TemporalLobe, ParietalLobe,
    Cerebellum, BrocasArea, Amygdala, CerebralCortex
)
from agents.brain.modules.hippocampus import Hippocampus
class CognitiveBrain(Brain):
    def __init__(self, toolkit, forget_threshold: int = 10, verbose: bool = True, memory_type='cuda'):
        super().__init__(toolkit, forget_threshold, verbose, memory_type)

        # Add cognitive modules to the brain
        self.modules = [
            PreFrontalCortex(),
            OccipitalLobe(),
            FrontalLobe(),
            TemporalLobe(),
            ParietalLobe(),
            Cerebellum(),
            BrocasArea(),
            Amygdala(),
            CerebralCortex(),
            Hippocampus(brain=self)
        ]