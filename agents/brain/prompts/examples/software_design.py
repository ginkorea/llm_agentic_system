# software_design_examples.py

from agents.brain.prompts.examples import ExamplesBase

class SoftwareDesignExamples(ExamplesBase):
    """
    Examples for the SoftwareDesignLobe, focused on generating UML diagrams and architecture designs.
    """

    def __init__(self):
        super().__init__()
        self.prd_example = self.get_prd_example()
        self.uml_output_example = self.get_uml_output_example()
        self.architecture_design_example = self.get_architecture_design_example()

    @staticmethod
    def get_prd_example() -> str:
        """
        Returns the sample PRD.
        """
        return """
        # Project Overview
        The `Task Tracker` application is designed to streamline task management for small teams, enabling members to create, assign, and track tasks with real-time updates. The system focuses on simplicity and efficiency.

        # Features
        1. **Task Management**: Users can create, assign, and update tasks with descriptions, priorities, and deadlines.
        2. **Team Collaboration**: Each team has a dashboard showing task status and team activity.
        3. **Notifications**: Alerts for approaching deadlines and task updates.

        # Constraints
        - Must support both desktop and mobile devices.
        - The system should handle up to 100 simultaneous users.

        # Technical Details
        - **Frontend**: ReactJS for cross-platform compatibility.
        - **Backend**: Node.js for task management APIs.
        - **Database**: PostgreSQL for secure and structured data storage.

        # Use Cases
        1. A team lead assigns tasks to members with deadlines and priorities.
        2. Team members update task progress and set task statuses to `In Progress` or `Complete`.
        3. A user receives notifications for approaching deadlines and task changes.
        """

    @staticmethod
    def get_uml_output_example() -> str:
        """
        Returns the UML diagram example.
        """
        return """
        # UMLDiagram.uml
        ```plaintext
        @startuml
        class User {
            +userID: int
            +name: string
            +email: string
        }

        class Task {
            +taskID: int
            +title: string
            +description: string
            +priority: string
            +deadline: date
            +status: string
        }

        class Team {
            +teamID: int
            +teamName: string
            +members: list<User>
        }

        User --> Task
        Team --> User
        Team --> Task
        @enduml
        ```
        """

    @staticmethod
    def get_architecture_design_example() -> str:
        """
        Returns the architecture design example.
        """
        return """
        # ArchitectureDesign.md
        ```plaintext
        ## Architecture Design for Task Tracker Application

        ### Components
        1. **Frontend**:
            - Framework: ReactJS
            - Features:
                - Task creation and assignment interface
                - Team dashboard for activity tracking
                - Real-time updates via WebSockets

        2. **Backend**:
            - Framework: Node.js with Express.js
            - Features:
                - API endpoints for task management and notifications
                - WebSocket server for real-time updates

        3. **Database**:
            - Type: PostgreSQL
            - Features:
                - Tables for Users, Tasks, and Teams
                - Indexing for fast queries on task deadlines and statuses

        4. **Deployment**:
            - Platform: AWS
            - Features:
                - Load Balancer for handling up to 100 simultaneous users
                - Autoscaling for traffic spikes

        5. **Third-Party Integrations**:
            - Notifications: Twilio for SMS and email alerts
        ```
        """

    def get_examples(self) -> str:
        """
        Concatenates the PRD example, UML output, and architecture design into one string.
        """
        return f"{self.get_prd()}\n\n{self.get_uml()}\n\n{self.get_architecture()}"
