import re
from typing import Optional, List, Dict
from agents.brain.prompts.examples.software_design_judge_examples import SoftwareDesignJudgeExamples
from agents.brain.prompts.structured.software_design_judge_prompt import SoftwareDesignJudgePrompt
from agents.brain.lobes.module import Module
from agents.brain.core import Brain


class SoftwareDesignJudge(Module):
    """Parses and evaluates raw UML Class Diagram, Sequence Diagram, and Architecture Design."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.4,
            memory_limit=3,
            system_message="You are a software design evaluator. Parse and evaluate UML Class Diagram, Sequence Diagram, and Architecture Design.",
        )
        self.examples = SoftwareDesignJudgeExamples()
        self.prompt_input = None

    @staticmethod
    def validate_uml_class(uml_class: str, required_classes: set) -> tuple[bool, str]:
        if not uml_class:
            return False, "UML Class Diagram is missing."
        defined_classes = set(re.findall(r"class (\w+)", uml_class))
        missing_classes = required_classes - defined_classes
        if missing_classes:
            return False, f"Missing classes: {', '.join(missing_classes)}"
        return True, "UML Class Diagram is valid."

    @staticmethod
    def validate_uml_sequence(uml_sequence: str) -> tuple[bool, str]:
        if not uml_sequence:
            return False, "UML Sequence Diagram is missing."
        
        return True, "UML Sequence Diagram is valid."

    @staticmethod
    def validate_architecture(architecture: str) -> tuple[bool, str]:
        if not architecture:
            return False, "Architecture Design is missing."

        return True, "Architecture Design is valid."

    def build_prompt_builder(self, brain: Optional[Brain] = None, raw_output: str = None, **kwargs) -> None:
        self.prompt_input = {
            "prd": brain.knowledge_base.get("prd", "PRD not found"),
            "uml_class": brain.knowledge_base.get("uml_class", "UML Class Diagram not found"),
            "uml_sequence": brain.knowledge_base.get("uml_sequence", "UML Sequence Diagram not found"),
            "architecture": brain.knowledge_base.get("architecture", "Architecture Design not found"),
        }
        self.prompt_builder = SoftwareDesignJudgePrompt(examples=self.examples.get_examples())
