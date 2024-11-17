from agents.brain.prompts.examples.software_design_judge_examples import SoftwareDesignJudgeExamples
from agents.brain.prompts.structured.software_design_judge_prompt import SoftwareDesignJudgePrompt
from agents.brain.lobes.module import Module
from typing import List, Dict, Optional
from agents.brain.core import Brain


class SoftwareDesignJudge(Module):
    """Parses and evaluates raw UML and Architecture Design outputs."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.4,
            memory_limit=3,
            system_message="You are a software design evaluator. Parse and evaluate UML and Architecture Design.",
        )
        self.examples = SoftwareDesignJudgeExamples()
        self.prompt_input = None

    @staticmethod
    def parse_output(raw_output: str) -> dict:
        """
        Parses raw output from the SoftwareDesigner into UML and Architecture sections.

        Parameters:
        - raw_output: The raw string output from the SoftwareDesigner.

        Returns:
        - A dictionary with keys `uml` and `architecture`, containing their respective content.
        """
        uml_start = raw_output.find("# UML Diagram")
        arch_start = raw_output.find("# Architecture Design")

        if uml_start == -1 or arch_start == -1:
            raise ValueError("Unable to parse UML or Architecture Design from raw output.")

        uml_end = arch_start  # UML ends where Architecture begins
        uml_content = raw_output[uml_start:uml_end].strip()
        arch_content = raw_output[arch_start:].strip()

        return {
            "uml": uml_content,
            "architecture": arch_content
        }

    def build_prompt_builder(self, brain: Optional[Brain] = None, raw_output: str = None, **kwargs) -> None:
        """
        Builds a structured prompt for evaluating designs after parsing.

        Parameters:
        - brain: The current Brain instance.
        """
        try:
            # Prepare the knowledge base for evaluation
            self.prompt_input = {
                "prd": brain.knowledge_base.get("prd", "PRD not found"),
                "uml": brain.knowledge_base.get("uml", "UML Diagram not found"),
                "architecture": brain.knowledge_base.get("architecture", "Architecture Design not found"),
            }
        except KeyError:
            self.prompt_input = {
                "prd": "PRD not found",
                "uml": "UML Diagram not found",
                "architecture": "Architecture Design not found",
            }

        self.prompt_builder = SoftwareDesignJudgePrompt(examples=self.examples.get_examples())

    def process(self, prompt_messages: List[Dict[str, str]] = None) -> str:
        """
        Process the input using the configured language model with a structured prompt.

        Parameters:
        - prompt_messages: A list of dictionaries containing the formatted prompt messages (optional).

        Returns:
        - The response content as a stripped string.
        """
        self.prompt_builder.build_prompt("", knowledge_base=self.prompt_input)
        response = self.model.invoke(self.prompt_builder.prompt)  # Pass prompt directly
        return response.content.strip()



