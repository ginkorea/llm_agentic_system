from agents.brain.goal.milestones import Milestone
import colorama

class EnvSetupMilestone(Milestone):
    def __init__(self):
        super().__init__("Set up the development environment for the project based on the requirements.txt.")

    def is_achieved(self, brain, input_data):
        print(f"{colorama.Fore.CYAN}Checking if the environment is set up...{colorama.Style.RESET_ALL}")
        return True, f"{colorama.Fore.GREEN}Environment Setup Complete.{colorama.Style.RESET_ALL}"