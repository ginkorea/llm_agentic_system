from agents.brain.prompts.examples import ExamplesBase


class EnvironmentSetupExamples(ExamplesBase):
    """
    Examples for the EnvironmentSetupManager, focused on generating dependency files.
    """

    def __init__(self):
        super().__init__()
        self.prd_example = self.get_prd_example()
        self.uml_example = self.get_uml_example()
        self.architecture_example = self.get_architecture_example()
        self.requirements_txt_example = self.get_requirements_txt_example()

    @staticmethod
    def get_prd_example() -> str:
        """
        Returns the sample PRD.
        """
        return """
        # Project Overview
        The `DataAnalyzer` application processes and visualizes large datasets.

        # Features
        1. Data ingestion and transformation.
        2. Integration with machine learning pipelines for model training.
        3. Customizable visualization tools.

        # Technical Details
        - **Programming Language**: Python
        - **Dependencies**:
            - Pandas for data manipulation.
            - NumPy for numerical computations.
            - Matplotlib for visualizations.

        # Use Cases
        - A data scientist preparing data for machine learning.
        - An analyst generating reports from datasets.
        """

    @staticmethod
    def get_uml_example() -> str:
        """
        Returns the UML diagram example.
        """
        return """
        ```plaintext
        @startuml
        class DataIngestion {
            +loadData(source: string): DataFrame
        }

        class DataTransformation {
            +transformData(data: DataFrame): DataFrame
        }

        class Visualization {
            +generateGraph(data: DataFrame, graphType: string): void
        }

        DataIngestion --> DataTransformation
        DataTransformation --> Visualization
        @enduml
        ```
        """

    @staticmethod
    def get_architecture_example() -> str:
        """
        Returns the Architecture Design example.
        """
        return """
        ```plaintext
        ## Architecture Design for DataAnalyzer Application

        ### Components
        1. **Frontend**:
            - Framework: ReactJS
            - Features: Data upload and visualization dashboard.

        2. **Backend**:
            - Framework: Flask
            - Features: Data processing and API endpoints.

        3. **Database**:
            - Type: PostgreSQL
            - Features: Storing processed datasets and user configurations.

        4. **Visualization**:
            - Libraries: Matplotlib and Plotly for graph generation.
        ```
        """

    @staticmethod
    def get_requirements_txt_example() -> str:
        """
        Returns an example requirements.txt file.
        """
        return """
        ```plaintext
        # requirements.txt
        pandas==1.3.3
        numpy==1.21.2
        matplotlib==3.4.3
        flask==2.0.1
        react==17.0.2
        plotly==5.3.1
        ```
        """

    def get_examples(self) -> str:
        """
        Concatenates the PRD example, UML diagram, architecture design, and requirements.txt example into one string.
        """
        return f"""
        # PRD Example
        {self.prd_example}

        # UML Diagram Example
        {self.uml_example}

        # Architecture Design Example
        {self.architecture_example}

        # Requirements.txt Example
        {self.requirements_txt_example}
        """
