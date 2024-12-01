import os
import re
from agents.brain.goal.milestones import Milestone
from agents.toolkit.create_virtual_environment import CreateVenvInput, create_virtualenv_with_requirements


class EnvSetupMilestone(Milestone):
    def __init__(self):
        super().__init__("Environment Setup Milestone")

    @staticmethod
    def parse_generated_files(input_data: str) -> dict:
        """
        Parses the generated output to extract filenames and file content.

        Args:
            input_data (str): The raw output from the LLM.

        Returns:
            dict: A dictionary with filenames as keys and content as values.
        """
        # Match file blocks: "# filename\n```<content>```"
        code_blocks = re.findall(r"# (\S+)\n```(?:\w+\n)?(.*?)```", input_data, re.DOTALL)

        # Remove trailing explanations or comments after code
        parsed_files = {filename: content.strip() for filename, content in code_blocks}
        return parsed_files

    def validate_environment(self, brain, parsed_files: dict) -> tuple[bool, str]:
        """
        Validates the environment setup based on the parsed files.

        Args:
            brain: The Brain instance managing the system's knowledge and tools.
            parsed_files (dict): A dictionary containing the filenames and their content.

        Returns:
            tuple: A boolean indicating success and a message.
        """
        # Validate `requirements.txt`
        if "requirements.txt" not in parsed_files:
            return False, "`requirements.txt` is missing from the generated files."

        # Save `requirements.txt`
        req_path = os.path.join(brain.work_folder, "requirements.txt")
        os.makedirs(os.path.dirname(req_path), exist_ok=True)
        with open(req_path, "w") as req_file:
            req_file.write(parsed_files["requirements.txt"])

        # Create virtual environment
        if os.path.exists("project_env"):
            # remove existing virtual environment directory
            os.system("rm -rf project_env")
        create_input = CreateVenvInput(env_name="project_env", requirements_file=req_path)
        passed, result = create_virtualenv_with_requirements.invoke({"input_data": create_input.model_dump()})

        if not passed:
            print(create_input.env_name, create_input.requirements_file)
            return False, f"Failed to set up virtual environment:\n{result}"

        # Save all files and structure
        for filename, content in parsed_files.items():
            if not filename.endswith(".py"):
                file_path = os.path.join(brain.work_folder, filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as f:
                    f.write(content)

        self.complete(brain.goal)
        return True, "Environment setup is complete. All files validated and saved."

    def is_achieved(self, brain, input_data) -> tuple[bool, str]:
        """
        Judges whether the milestone is achieved based on the LLM-generated output.

        Args:
            brain: The Brain instance managing the system's knowledge and tools.
            input_data (str): The raw output from the LLM module.

        Returns:
            tuple: A boolean indicating success and a message.
        """
        parsed_files = self.parse_generated_files(input_data)

        if not parsed_files:
            return False, "No valid files were generated by the LLM. Please retry environment setup."

        return self.validate_environment(brain, parsed_files)
