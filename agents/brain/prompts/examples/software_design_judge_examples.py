# software_design_judge_examples.py
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
        - UML Diagram: Missing key classes (e.g., User). Cardinality is not specified.
        - Architecture Design: Does not mention real-time updates via WebSockets.
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
