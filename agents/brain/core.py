from .memory import Memory
from .lobes import PreFrontalCortex, OccipitalLobe, TemporalLobe, ParietalLobe, Cerebellum, Hippocampus, BrocasArea, Amygdala, CerebralCortex


from .memory import Memory
from .lobes import PreFrontalCortex, TemporalLobe

class Brain:
    def __init__(self, forget_threshold: int = 10):
        self.memory = Memory(forget_threshold=forget_threshold)

        # Initialize lobes
        self.prefrontal_cortex = PreFrontalCortex()
        self.temporal_lobe = TemporalLobe()

        # Add lobes to a list with prefrontal cortex at index 0 and temporal lobe at index -1
        self.lobes = [self.prefrontal_cortex, self.temporal_lobe]

    def store_memory(self, user_input: str, response: str):
        """Store the user input and response in the brain's memory."""
        self.memory.short_term.append({"user_input": user_input, "response": response})
        if len(self.memory.short_term) > self.memory.forget_threshold:
            self.memory.short_term.pop(0)

    def determine_lobe(self, user_input: str, reasoning: bool) -> int:
        """
        Determine which lobe to use based on the input and reasoning flag.
        Standard index selection: 0 (PreFrontalCortex) or -1 (TemporalLobe).
        """
        if reasoning:
            return 0  # PreFrontalCortex for reasoning
        return -1  # TemporalLobe for memory recall or language comprehension

    def process_input(self, user_input: str, reasoning: bool = False) -> str:
        """Process input using the appropriate lobe and the brain's memory."""
        lobe_index = self.determine_lobe(user_input, reasoning)
        selected_lobe = self.lobes[lobe_index]
        # Process input using the selected lobe and send the short-term memory
        return selected_lobe.process(user_input, self.memory.short_term)

class AdvancedBrain(Brain):
    def __init__(self, forget_threshold: int = 25):
        super().__init__(forget_threshold=forget_threshold)

        # Initialize additional lobes for advanced tasks
        self.frontal_lobe = FrontalLobe()
        self.occipital_lobe = OccipitalLobe()
        self.parietal_lobe = ParietalLobe()
        self.cerebellum = Cerebellum()
        self.hippocampus = Hippocampus()
        self.brocas_area = BrocasArea()
        self.amygdala = Amygdala()
        self.cerebral_cortex = CerebralCortex()

        # Add lobes in a list, keeping prefrontal cortex at index 0 and temporal lobe at index -1
        self.lobes = [
            self.prefrontal_cortex,  # index 0
            self.frontal_lobe,
            self.occipital_lobe,
            self.parietal_lobe,
            self.cerebellum,
            self.hippocampus,
            self.brocas_area,
            self.amygdala,
            self.cerebral_cortex,
            self.temporal_lobe  # index -1
        ]

    def determine_lobe(self, user_input: str, reasoning: bool) -> int:
        """
        Determine which lobe to use for advanced reasoning based on the input.
        Return the appropriate index for the lobe list.
        """
        if "visual" in user_input or "pattern" in user_input:
            return 2  # OccipitalLobe
        elif "math" in user_input or "code" in user_input:
            return 3  # ParietalLobe
        elif "memory" in user_input or reasoning:
            return 1  # FrontalLobe
        elif "emotion" in user_input or "feelings" in user_input:
            return 7  # Amygdala
        else:
            return 0  # Default to PreFrontalCortex for quick decisions
