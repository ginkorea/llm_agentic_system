from agents.brain.prompts.examples import ExamplesBase

class SoftwareDesignJudgeExamples(ExamplesBase):
    """
    Examples for evaluating UML and Architecture designs based on PRD.
    """

    def __init__(self):
        super().__init__()
        self.prd_example = self.get_prd_example()
        self.uml_example = self.get_uml_example()
        self.architecture_example = self.get_architecture_example()
        self.feedback_example = self.get_feedback_example()

    @staticmethod
    def get_prd_example() -> str:
        return """
        # Project Overview
        The `Task Tracker` application is designed to streamline task management for small teams.

        # Features
        - Task Management: Create, assign, and update tasks.
        - Team Collaboration: Dashboard for task status.
        - Notifications: Alerts for approaching deadlines.

        # Technical Details
        - Frontend: ReactJS
        - Backend: Node.js
        - Database: PostgreSQL
        """

    @staticmethod
    def get_uml_example() -> str:
        return """
        ```plaintext
        @startuml
        class Task {
            +taskID: int
            +title: string
        }

        class Team {
            +teamID: int
        }

        Task --> Team
        @enduml
        ```
        """

    @staticmethod
    def get_architecture_example() -> str:
        return """
        ```plaintext
        ## Architecture Design for Task Tracker Application

        ### Components
        1. **Frontend**: ReactJS
        2. **Backend**: Node.js
        3. **Database**: PostgreSQL
        ```
        """

    @staticmethod
    def get_feedback_example() -> str:
        return """
        Feedback:
        [
            {
                "type": "uml",
                "score": 0.85,
                "pass/fail": "pass",
                "reason": "All key classes and relationships are defined. Cardinality is specified for all associations.",
                "recommendation": "No major changes needed. Consider improving the readability of class names."
            },
            {
                "type": "architecture",
                "score": 0.65,
                "pass/fail": "fail",
                "reason": "Real-time updates via WebSockets are not mentioned, and the deployment strategy is incomplete.",
                "recommendation": "Add details about WebSocket integration for real-time updates and specify the deployment strategy."
            }
        ]
        """

    def get_examples(self) -> str:
        return f"""
        # PRD Example
        {self.prd_example}

        # UML Diagram Example
        {self.uml_example}

        # Architecture Design Example
        {self.architecture_example}

        # Feedback Example
        {self.feedback_example}
        """
