import os
import re
import colorama
from agents.brain.goal.milestones import Milestone
from agents.toolkit.create_virtual_environment import create_virtualenv_with_requirements, CreateVenvInput

class EnvSetupMilestone(Milestone):
    def __init__(self):
        super().__init__("Create and set up the environment and files based on the PRD and Architecture Design.")

    @staticmethod
    def parse_files(input_data: str) -> dict:
        """
        Parses the input to extract filenames, paths, and content.

        Args:
            input_data (str): Raw output containing files.

        Returns:
            dict: A dictionary where keys are file paths and values are file content.
        """
        file_blocks = re.findall(r"# ([^\n]+)\n```(.*?)\n(.*?)```", input_data, re.DOTALL)
        files = {filename.strip(): content.strip() for filename, _, content in file_blocks}
        return files

    def is_achieved(self, brain, input_data: str) -> tuple[bool, str]:
        """
        Parses, validates, and saves files, then sets up the virtual environment.

        Parameters:
        - brain: The Brain instance managing the system's knowledge and tools.
        - input_data: The raw output from the `EnvironmentSetupManager`.

        Returns:
        - Tuple[bool, str]: A tuple containing:
            - A boolean indicating if the milestone was achieved.
            - A string with the success or error message.
        """
        green = colorama.Fore.GREEN
        red = colorama.Fore.RED
        cyan = colorama.Fore.CYAN
        reset = colorama.Style.RESET_ALL

        try:
            print(f"{cyan}Parsing the output for files...{reset}")
            files = self.parse_files(input_data)
            if not files:
                return False, f"{red}No valid files found in the output. Please ensure the output is correctly formatted.{reset}"

            # Save files to the appropriate directory
            for file_path, content in files.items():
                full_path = os.path.join(brain.work_folder, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w") as f:
                    f.write(content)
                print(f"{green}Saved file: {full_path}{reset}")

            # Validate and install requirements.txt
            if "requirements.txt" in files:
                requirements_path = os.path.join(brain.work_folder, "requirements.txt")
                create_input = CreateVenvInput(env_name="project_env", requirements_file=requirements_path)
                result = create_virtualenv_with_requirements.invoke({"input_data": create_input.model_dump()})

                if "successfully" in result:
                    brain.knowledge_base["requirements.txt"] = files["requirements.txt"]
                    print(f"{green}Virtual environment created successfully.{reset}")
                else:
                    return False, f"{red}Failed to set up virtual environment: {result}{reset}"

            # Save files to knowledge base
            brain.knowledge_base.setdefault("files", {}).update(files)

            return True, f"{green}Environment setup complete with all files saved successfully.{reset}"
        except Exception as e:
            return False, f"{red}An error occurred during environment setup: {e}{reset}"
