import colorama
from agents.brain.goal.milestones import Milestone
from agents.toolkit.create_virtual_environment import create_virtualenv_with_requirements, CreateVenvInput


class EnvSetupMilestone(Milestone):
    def __init__(self):
        super().__init__("Set up the development environment for the project based on the requirements.txt.")

    def is_achieved(self, brain, input_data) -> tuple[bool, str]:
        """
        Checks if the `requirements.txt` is valid and sets up the virtual environment.

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
            print(f"{cyan}Validating the output from the EnvironmentSetupManager...{reset}")

            # Validate input_data as a requirements.txt
            if not input_data.strip().startswith("#") and "==" not in input_data:
                return False, f"{red}The provided requirements.txt is invalid. Please check the format.{reset}"

            # Save the requirements.txt to the brain's work folder
            requirements_path = f"{brain.work_folder}/requirements.txt"
            with open(requirements_path, "w") as req_file:
                req_file.write(input_data)

            print(f"{cyan}Requirements.txt saved successfully: {requirements_path}{reset}")

            # Create a virtual environment using the tool
            create_input = CreateVenvInput(env_name="project_env", requirements_file=requirements_path)
            result = create_virtualenv_with_requirements.invoke({"input_data": create_input.model_dump()})

            # Check the result
            if "successfully" in result:
                brain.knowledge_base["requirements.txt"] = input_data
                return True, f"{green}Virtual environment created and requirements installed successfully.{reset}"
            else:
                return False, f"{red}Failed to create virtual environment: {result}{reset}"

        except Exception as e:
            return False, f"{red}An error occurred: {e}{reset}"
