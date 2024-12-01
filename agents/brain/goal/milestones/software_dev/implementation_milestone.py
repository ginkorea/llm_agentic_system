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

        parsed_files = {}
        for pre_filename, code, post_filename in code_blocks:
            filename = pre_filename or post_filename
            if filename:
                parsed_files[filename.strip()] = code.strip()

        # If no valid code blocks are found, use fallback parsing
        if not parsed_files:
            parsed_files = ImplementationMilestone.fallback_parse_code_files(input_data)

        return parsed_files

    @staticmethod
    def fallback_parse_code_files(input_data):
        """
        Fallback parser to extract code blocks using generic ``` delimiters.

        Args:
            input_data (str): Raw response containing multiple code blocks.

        Returns:
            dict: A dictionary where keys are generic filenames and values are code strings.
        """
        code_blocks = re.findall(r"```(?:python)?\n(.*?)```", input_data, re.DOTALL)

        # Use generic filenames if no filename is provided
        parsed_files = {}
        for i, code in enumerate(code_blocks, start=1):
            parsed_files[f"file_{i}.py"] = code.strip()

        return parsed_files

    @staticmethod
    def save_code_files(brain, code_files, work_folder):
        """
        Saves code files to the brain's knowledge base and the file system.

        Args:
            brain: The Brain instance managing the system's knowledge and tools.
            code_files (dict): Dictionary of filenames and their code content.
            work_folder (str): Directory to save the code files.
        """
        if "code" not in brain.knowledge_base:
            brain.knowledge_base.setdefault("code", {})

        for filename, code in code_files.items():
            filename = filename.replace(work_folder + "/", "")  # remove work_folder from filename
            # Save to the knowledge base
            brain.knowledge_base["code"][filename] = code

            # Save to the file system
            file_path = os.path.join(work_folder, filename)

            # Print the filename in green and the code in blue
            ImplementationMilestone.save_file_print_green_name_and_blue_text(file_path, code)

        # Print the entire brain.knowledge_base["code"] dictionary in yellow
        print("\033[33m", brain.knowledge_base["code"], "\033[0m")

    @staticmethod
    def save_file_print_green_name_and_blue_text(file_path, code):
        """
        Saves the code to the file and prints the filename in green and the code in blue.

        Args:
            file_path (str): The path to the file.
            code (str): The code to save.
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(code)
        print("\033[32m", file_path, "\033[0m")
        print("\033[34m", code, "\033[0m")

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
        if not code_files:
            return False, ("No code files were found in the input data. Please ensure the code is generated correctly. \n"
                           "Code Produced (first 100 chars): \n" + input_data[:100])

        # Save all code files to the brain's knowledge base and working directory
        self.save_code_files(brain, code_files, brain.work_folder)

        # Extract required classes from the UML Class Diagram
        uml_class_diagram = brain.knowledge_base.get("uml_class", "")
        required_classes = set(re.findall(r"class (\w+)", uml_class_diagram))
        if not required_classes:
            return False, "No required classes found in the UML Class Diagram."

        # Extract implemented classes from the saved code files
        implemented_classes = set()
        for code in brain.knowledge_base["code"].values():
            implemented_classes.update(self.extract_classes_from_code(code))

        # Determine missing classes
        missing_classes = required_classes - implemented_classes
        if missing_classes:
            brain.knowledge_base["missing_classes"] = list(missing_classes)
            return False, (
                f"The following classes are missing: {', '.join(missing_classes)}. "
                "Partial files have been saved for future iterations."
            )

        main_file = brain.knowledge_base['code'].get('main.py', '')
        if not main_file:
            return False, "No main.py file found in the code. Please ensure the main flow is tested in a separate `test_main.py` file."

        # If all requirements are met
        self.complete(brain.goal)
        return True, "All required classes have been implemented and saved. Proceed to the next milestone."
