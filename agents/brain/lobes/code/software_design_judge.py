# software_design_judge.py
from agents.brain.prompts.examples import SoftwareDesignJudgeExamples
from agents.brain.prompts.structured import SoftwareDesignJudgePrompt
from agents.brain.lobes.module import Module
from typing import Optional
from agents.brain.core import Brain

class SoftwareDesignJudge(Module):
    """
    Judges the suitability of UML and Architecture designs based on the PRD.
    """

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=5,
            system_message="Evaluate UML and Architecture designs based on the PRD.",
        )
        self.examples = SoftwareDesignJudgeExamples()
        self.prompt_input = None

    def build_prompt_builder(self, brain: Optional[Brain] = None, modules=None, tools=None, examples=None):
        """
        Builds the structured prompt for design evaluation.
        """
        if brain and brain.knowledge_base:
            prd = brain.knowledge_base.get("prd", "").strip()
            uml = brain.knowledge_base.get("uml", "").strip()
            architecture = brain.knowledge_base.get("architecture", "").strip()

            if not prd or not uml or not architecture:
                raise ValueError("Missing required inputs in the knowledge base.")

            self.prompt_builder = SoftwareDesignJudgePrompt(examples=self.examples.get_examples())
            self.prompt_input = self.prompt_builder.build_prompt(prd, uml, architecture)

    def process_input(self, brain: Brain) -> str:
        """
        Evaluates the designs based on the PRD and feedback criteria.
        """
        self.build_prompt_builder(brain=brain)
        return self.model.invoke(self.prompt_input).content.strip()
