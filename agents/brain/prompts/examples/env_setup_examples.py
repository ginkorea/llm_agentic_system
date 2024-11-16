# env_setup_examples.py

from agents.brain.prompts.examples import ExamplesBase

class EnvironmentSetupExamples(ExamplesBase):
    """
    Examples for the EnvironmentSetupManager, focused on generating dependency files.
    """

    def __init__(self):
        super().__init__()
        self.prd_example = self.get_prd_example()
        self.requirements_txt_example = self.get_requirements_txt_example()

    @staticmethod
    def get_prd_example() -> str:
        """
        Returns the sample PRD.
        """
        return """
        # Project Overview
        The `DataProcessor` application is designed to process and analyze large datasets efficiently.

        # Features
        1. Data ingestion from various sources like CSV, JSON, and databases.
        2. Real-time data processing and transformation.
        3. Integration with machine learning pipelines for model training.

        # Technical Details
        - **Programming Language**: Python
        - **Dependencies**:
            - Pandas for data manipulation.
            - NumPy for numerical computations.
            - Scikit-learn for machine learning models.
            - SQLAlchemy for database interactions.
            - Matplotlib for data visualization.

        # Use Cases
        - A data scientist preparing a dataset for model training.
        - An analyst visualizing trends in the data.
        """

    @staticmethod
    def get_requirements_txt_example() -> str:
        """
        Returns an example requirements.txt file.
        """
        return """
        # requirements.txt
        pandas==1.3.3
        numpy==1.21.2
        scikit-learn==0.24.2
        SQLAlchemy==1.4.22
        matplotlib==3.4.3
        """

    def get_examples(self) -> str:
        """
        Concatenates the PRD example and requirements.txt example into one string.
        """
        return f"{self.prd_example}\n\n{self.requirements_txt_example}"
