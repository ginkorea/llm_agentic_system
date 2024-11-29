from agents.brain.prompts.examples import ExamplesBase

class SoftwareDesignJudgeExamples(ExamplesBase):
    """
    Examples for evaluating UML and Architecture designs based on PRD.
    """

    def __init__(self):
        super().__init__()
        self.feedback_example = self.get_expanded_feedback()

    @staticmethod
    def get_uml_feedback() -> str:
        """
        Feedback for UML Class and Sequence diagrams.
        """
        return f"""
        UML Class Feedback:
        {{
            "type": "uml_class",
            "score": 0.90,
            "pass/fail": "pass",
            "reason": "Classes such as InventoryManager, Item, and Location are well-defined, with appropriate methods and attributes. Relationships between classes are correctly represented, and cardinality is specified for associations.",
            "recommendation": "Consider improving the naming conventions of some methods to better reflect their purpose, and ensure consistent documentation for all methods."
        }}

        UML Sequence Feedback:
        {{
            "type": "uml_sequence",
            "score": 0.85,
            "pass/fail": "pass",
            "reason": "The sequence diagram effectively captures user interactions with the system, including inventory queries and updates. Actors and participants are clearly identified, and key interactions are outlined.",
            "recommendation": "Add error-handling flows, such as cases where inventory queries fail or updates are invalid, to make the diagram more comprehensive."
        }}
        """

    @staticmethod
    def get_architecture_feedback() -> str:
        """
        Feedback for Architecture Design.
        """
        return f"""
        Architecture Feedback:
        {{
            "type": "architecture",
            "score": 0.75,
            "pass/fail": "pass",
            "reason": "The architecture includes a robust separation of concerns with distinct components for the frontend (React.js), backend (Flask), and database (PostgreSQL). However, details on WebSocket integration for real-time updates are missing.",
            "recommendation": "Include specifics about how the WebSocket server will interact with the backend and clients. Additionally, provide a detailed deployment strategy, including hosting and scalability considerations."
        }}
        """

    def get_expanded_feedback(self) -> str:
        """
        Consolidated expanded feedback including UML Class, UML Sequence, and Architecture.
        """
        return f"""
        # Consolidated Feedback

        ## UML Class Diagram Feedback
        {self.get_uml_feedback()}

        ## UML Sequence Diagram Feedback
        {self.get_uml_feedback()}

        ## Architecture Design Feedback
        {self.get_architecture_feedback()}
        """

    def get_examples(self) -> str:
        return f"""
        # PRD Example
        {self.get_prd()}

        # UML Class Diagram Example
        {self.get_uml_class()}

        # UML Sequence Diagram Example
        {self.get_uml_sequence()}

        # Architecture Design Example
        {self.get_architecture()}

        # Feedback Example
        {self.feedback_example}
        """
