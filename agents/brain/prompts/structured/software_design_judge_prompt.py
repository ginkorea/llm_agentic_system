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
        - Analyze the provided UML Class and Sequence Diagrams and Architecture Design.
        - Evaluate their alignment with the PRD and their adherence to design principles.
        - Provide feedback on strengths and areas for improvement.

        Your evaluation criteria include:
        - Faithfulness: Alignment with PRD.
        - Cohesion and Decoupling: High cohesion within components, low coupling between them.
        - Practicability: Clear, modular, and efficient design.
        - Conformance: Adherence to community and industry standards.

        Provide your feedback in a structured JSON format with the following fields:
        - `type`: Specify if the evaluation is for "uml_class", "uml_sequence", or "architecture".
        - `score`: A numeric value between 0 and 1 indicating the evaluation score.
        - `pass/fail`: Indicate "pass" if the score is 0.7 or higher, otherwise "fail".
        - `reason`: Describe the rationale behind the given score.
        - `recommendation`: Suggest actionable steps for improvement.

        """

    def build_prompt(
            self,
            prompt_input: str,
            previous_output: bool = False,
            previous_module: Optional[str] = None,
            goal: Goal = None,
            knowledge_base: dict = None,
    ) -> str:
        """
        Builds the prompt for evaluating UML and Architecture designs.
        """
        self.prompt = f"""
        {self.base_prompt}

        Example Inputs and Outputs:
        ----------------
        {self.examples}

        ----------------
        The examples above are for reference only. Your evaluation should be based on the provided input. 
        You should provide as much detail as possible in your evaluation.

        Analyze the following UML Diagram and Architecture Design based on the provided PRD:

        PRD:
        {knowledge_base.get("prd", "PRD not found")}

        UML Class Diagram:
        {knowledge_base.get("uml_class", "UML Class Diagram not found")}
        
        UML Sequence Diagram:
        {knowledge_base.get("uml_sequence", "UML Sequence Diagram not found")}

        Architecture Design:
        {knowledge_base.get("architecture", "Architecture Design not found")}

        ----------------

        Provide your feedback below in the structured JSON format as described above:
        """
        return self.prompt

