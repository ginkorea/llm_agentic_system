# software_design_judge_prompt.py
from agents.brain.prompts.structured.structured_prompt import StructuredPrompt
from typing import Optional
from agents.brain.goal.goal import Goal

class SoftwareDesignJudgePrompt(StructuredPrompt):
    """
    Specialized prompt for evaluating UML and Architecture designs.
    """

    def __init__(self, examples=None):
        super().__init__(examples=examples)
        self.base_prompt = """
        You are an expert in software design evaluation. Your task is to:
        - Analyze the provided UML Diagram and Architecture Design.
        - Evaluate their alignment with the PRD and their adherence to design principles.
        - Provide feedback on strengths and areas for improvement.

        Your evaluation criteria include:
        - Faithfulness: Alignment with PRD.
        - Cohesion and Decoupling: High cohesion within components, low coupling between them.
        - Practicability: Clear, modular, and efficient design.
        - Conformance: Adherence to community and industry standards.

        Provide your feedback in a structured format.
        """

    def build_prompt(self, prompt_input: str, previous_output: bool = False, previous_module: Optional[str] = None, goal: Goal = None) -> str:
        return f"""
        {self.base_prompt}

        Example Inputs and Outputs:
        ----------------
        {self.examples}

        ----------------

        PRD:
        {prd_text}

        UML Diagram:
        {uml_text}

        Architecture Design:
        {architecture_text}

        ----------------

        Provide your feedback below:
        """
