from agents.brain.core import Brain
from agents.brain.lobes.cognitive.lobes import (
    PreFrontalCortex, OccipitalLobe, FrontalLobe, TemporalLobe, ParietalLobe,
    Cerebellum, BrocasArea, Amygdala, CerebralCortex
)
from agents.brain.lobes.cognitive.hippocampus import Hippocampus
from agents.brain.prompts.examples.cognitive_examples import CognitiveExamples
class CognitiveBrain(Brain):
    def __init__(self, toolkit, forget_threshold: int = 10, verbose: bool = True, memory_type='cuda', goal_file=None, goal=None):
        super().__init__(toolkit, forget_threshold, verbose, memory_type, goal_file=goal_file, goal=goal)

        # Add cognitive lobes to the brain
        self.modules = [
            PreFrontalCortex(),
            FrontalLobe(),
            OccipitalLobe(),
            TemporalLobe(),
            ParietalLobe(),
            Cerebellum(),
            BrocasArea(),
            Amygdala(),
            CerebralCortex(),
            Hippocampus(brain=self)
        ]

        # Pre-generate descriptions for tools and modules
        self.tool_descriptions = self.build_tool_descriptions()
        self.module_descriptions = self.build_module_descriptions(include_routing_module=True)
        self.examples = CognitiveExamples()
        self.router = self.modules[0]