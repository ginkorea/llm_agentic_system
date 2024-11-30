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
        # Match patterns where the filename comment may be before or after the code block
        code_blocks = re.findall(
            r"(?:# (\S+)\n)?```python\n(.*?)```(?:\n# (\S+))?",
            input_data,
            re.DOTALL
        )

        # Process matches to extract filename and code content
        parsed_files = {}
        for pre_filename, code, post_filename in code_blocks:
            filename = pre_filename or post_filename
            if filename:
                parsed_files[filename.strip()] = code.strip()

        # print in green the parsed files
        for key, value in parsed_files.items():
            print(f"\033[92m{key}\033[00m")
            print(value)
            print()

        return parsed_files

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

    @staticmethod
    def save_code_files(brain, code_files):
        """
        Saves code files to the brain's knowledge base and the file system.

        Args:
            brain: The Brain instance managing the system's knowledge and tools.
            code_files (dict): Dictionary of filenames and their code content.
        """
        brain.knowledge_base.setdefault("code", {})
        for filename, code in code_files.items():
            brain.knowledge_base["code"][filename] = code
            file_path = os.path.join(brain.work_folder, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(code)

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
        self.save_code_files(brain, code_files)

        required_classes = brain.knowledge_base.get("required_classes", set())
        implemented_classes = set()

        # Gather implemented classes from all saved code files
        for code in brain.knowledge_base["code"].values():
            implemented_classes.update(self.extract_classes_from_code(code))

        # Determine missing classes
        missing_classes = required_classes - implemented_classes
        if missing_classes:
            # Add missing classes to brain.knowledge_base for focus in next iteration
            brain.knowledge_base["missing_classes"] = list(missing_classes)
            return False, (
                f"The following classes are missing: {', '.join(missing_classes)}. "
                f"Partial files saved for future iterations. Rework the implementation focusing on the missing classes."
            )

        for filename, code in brain.knowledge_base["code"].items():
            class_file_path = os.path.join(brain.work_folder, filename)
            with open(class_file_path, "w") as class_file:
                class_file.write(code)



        # If all requirements are met
        return True, "All required classes and main.py are implemented and saved. Proceed to developing and running unit tests."


