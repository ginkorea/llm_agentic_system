import os
import re
from agents.brain.goal.milestones import Milestone
from agents.toolkit.run_code_in_virtual_environment import CodeRunner
from agents.toolkit.create_virtual_environment import create_virtualenv_with_requirements, CreateVenvInput


class TestMilestone(Milestone):
    def __init__(self, name: str, test_type: str, knowledge_key: str, test_dir_suffix: str, predefined_dependencies: list[str]):
        """
        Initializes the base TestMilestone class.

        Args:
            name (str): The name of the milestone.
            test_type (str): The type of test (e.g., "Acceptance" or "Unit").
            knowledge_key (str): The key to store/retrieve test files in brain.knowledge_base.
            test_dir_suffix (str): The subdirectory suffix for the test files.
            predefined_dependencies (list[str]): A list of dependencies to install in the virtual environment.
        """
        super().__init__(name)
        self.test_type = test_type
        self.knowledge_key = knowledge_key
        self.test_dir_suffix = test_dir_suffix
        self.predefined_dependencies = predefined_dependencies
        self.env_name = "project_env"

    @staticmethod
    def parse_tests(input_data: str) -> dict:
        """
        Parses the input to extract filenames and test code.

        Args:
            input_data (str): Raw test data.

        Returns:
            dict: A dictionary where keys are filenames and values are test code strings.
        """
        # Match patterns where the filename may be before the code block or as the first line inside the block
        test_blocks = re.findall(
            r"(?:# (\S+)\n)?```python\n(?:# (\S+)\n)?(.*?)```",
            input_data,
            re.DOTALL
        )

        # Process matches to extract filename and code content
        parsed_files = {}
        for pre_filename, inline_filename, code in test_blocks:
            filename = pre_filename or inline_filename  # Use the first non-None filename
            if filename:
                parsed_files[filename.strip()] = code.strip()

        return parsed_files

    def save_tests(self, brain, test_files: dict) -> str:
        """
        Saves test files to the brain's knowledge base and the file system.

        Args:
            brain: The Brain instance managing the system's knowledge and tools.
            test_files (dict): Dictionary of test filenames and their content.

        Returns:
            str: The directory where test files were saved.
        """
        brain.knowledge_base.setdefault(self.knowledge_key, {})
        test_dir = os.path.join(brain.work_folder, f"tests/{self.test_dir_suffix}")
        os.makedirs(test_dir, exist_ok=True)

        for filename, test_code in test_files.items():
            # Update knowledge base
            brain.knowledge_base[self.knowledge_key][filename] = test_code

            # Save to the working directory
            name_start_index = filename.rfind("/") + 1
            filename = filename[name_start_index:]
            test_file_path = os.path.join(test_dir, filename)
            with open(test_file_path, "w") as f:
                f.write(test_code)

        return test_dir

    def install_dependencies(self) -> str:
        """
        Creates a virtual environment and installs predefined dependencies.

        Returns:
            str: Output of the installation process.
        """
        # Generate a temporary requirements.txt file for dependencies
        requirements_file = "requirements_temp.txt"
        with open(requirements_file, "w") as f:
            f.write("\n".join(self.predefined_dependencies))

        # Use create_virtualenv_with_requirements tool for installation
        create_input = CreateVenvInput(env_name=self.env_name, requirements_file=requirements_file)
        result = create_virtualenv_with_requirements.invoke({"input_data": create_input.dict()})

        # Clean up temporary requirements file
        os.remove(requirements_file)

        return result

    @staticmethod
    def run_tests(test_dir: str) -> str:
        """
        Runs the tests using CodeRunner.

        Args:
            test_dir (str): The directory containing the test files.

        Returns:
            str: The output of the test execution.
        """
        # Add workbench to PYTHONPATH
        os.environ["PYTHONPATH"] = os.getcwd()

        runner = CodeRunner(env_name="project_env")
        return runner.run(
            file_path="pytest",
            arguments=[test_dir, "--maxfail=5", "--disable-warnings", "-v"],  # Verbose output for detailed errors
        )

    @staticmethod
    def extract_errors(test_output: str) -> str:
        """
        Extracts detailed error messages from the pytest output.

        Args:
            test_output (str): The output from pytest.

        Returns:
            str: Extracted error messages.
        """
        error_pattern = re.compile(r"FAILED.*?\n(.*?\n)+", re.MULTILINE)
        errors = error_pattern.findall(test_output)
        return "\n".join(errors) if errors else "No detailed errors found."

    def is_achieved(self, brain, input_data: str) -> tuple[bool, str]:
        """
        Validates tests by saving, running, and checking results.

        Args:
            brain: The Brain instance managing the system's knowledge and tools.
            input_data: Test data generated by the respective test generator.

        Returns:
            tuple[bool, str]: (bool, str) indicating success and a message.
        """
        print(f"Validating {self.test_type} tests...")
        # Parse the input test data
        test_files = self.parse_tests(input_data)

        if not test_files:
            return False, f"No {self.test_type.lower()} tests found in the input data."

        # Save test files
        test_dir = self.save_tests(brain, test_files)

        # Install predefined dependencies
        install_output = self.install_dependencies()
        if "Error" in install_output:
            return False, f"Dependency installation failed:\n{install_output}"

        # Run the tests
        result = self.run_tests(test_dir)

        # Provide detailed feedback on test results
        if "failed" not in result:
            self.complete(brain.goal)
            return True, f"All {self.test_type.lower()} tests passed successfully.\n{result}"
        else:
            # Extract detailed errors
            detailed_errors = self.extract_errors(result)
            return False, f"Some {self.test_type.lower()} tests failed:\n\n{detailed_errors}\n\nFull Output:\n{result}"
