import os
import re
from agents.brain.goal.milestones import Milestone


class ImplementationMilestone(Milestone):
    def __init__(self):
        super().__init__("Code Implementation Milestone")

    @staticmethod
    def parse_code_files(input_data):
        """
        Parses the input to extract filenames and code blocks.

        Args:
            input_data (str): Raw response containing multiple code blocks.

        Returns:
            dict: A dictionary where keys are filenames and values are code strings.
        """
        code_blocks = re.findall(r"# (\S+)\n```python\n(.*?)```", input_data, re.DOTALL)
        return {filename: code.strip() for filename, code in code_blocks}

    @staticmethod
    def extract_classes_from_code(code):
        """
        Extracts class names from the given code.

        Args:
            code (str): Python code as a string.

        Returns:
            list: List of class names found in the code.
        """
        return re.findall(r"class (\w+)", code)


    def is_achieved(self, brain, input_data) -> tuple[bool, str]:
        """
        Validates the implementation against the UML Class Diagram.

        Args:
            brain: The Brain instance managing the system's knowledge and tools.
            input_data (str): Raw output from the CodeWriter module.

        Returns:
            tuple: (bool, str) indicating success and message.
        """
        # Parse response for code files
        code_files = self.parse_code_files(input_data)

        # Save all code files to brain knowledge base and working directory
        brain.knowledge_base.setdefault("code", {})
        for filename, code in code_files.items():
            brain.knowledge_base["code"][filename] = code
            file_path = os.path.join(brain.work_folder, filename)
            with open(file_path, "w") as f:
                f.write(code)

        required_classes = brain.knowledge_base.get("required_classes", set())

        # Gather implemented classes from knowledge base
        implemented_classes = set()
        for code in brain.knowledge_base["code"].values():
            implemented_classes.update(self.extract_classes_from_code(code))

        # Determine missing classes
        missing_classes = required_classes - implemented_classes
        if missing_classes:
            # Add missing classes to brain.knowledge_base for focus in next iteration
            brain.knowledge_base["missing_classes"] = list(missing_classes)
            return False, (
                f"The following classes are missing: {', '.join(missing_classes)}. "
                f"Partial files saved for future iterations.  Rework the implementation focusing on the full implementation for missing classes."
            )

        # Check for the presence of main.py
        if "main.py" not in brain.knowledge_base["code"]:
            brain.knowledge_base["missing_classes"] = ["main.py"]
            return False, "main.py is missing. Ensure the main entry point is implemented."

        # If all requirements are met
        return True, "All required classes and main.py are implemented and saved. Proceed to developing and running unit tests."

