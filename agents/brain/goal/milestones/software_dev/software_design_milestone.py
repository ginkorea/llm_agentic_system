import json
import colorama
from agents.brain.goal.milestones import Milestone

class SoftwareDesignMilestone(Milestone):
    def __init__(self):
        super().__init__("Complete UML and Architecture Design")

    def is_achieved(self, brain, _input_data) -> tuple[bool, str]:
        """
        Checks if the UML and Architecture Design are valid and stores their code blocks in the knowledge base.

        Parameters:
        - brain: The Brain instance managing the system's knowledge and modules.
        - input_data: The raw output from the SoftwareDesigner module.

        Returns:
        - Tuple[bool, str]: A tuple containing:
            - A boolean indicating if the milestone was achieved.
            - A string with a refined prompt for the next step.
        """
        green = colorama.Fore.GREEN
        red = colorama.Fore.RED
        cyan = colorama.Fore.CYAN
        reset = colorama.Style.RESET_ALL

        print(f"{cyan}Checking UML and Architecture Design validity and storing in the knowledge base.{reset}")
        uml, architecture = SoftwareDesignMilestone.parse_input_data(_input_data)
        if uml != "" and architecture != "":
            brain.knowledge_base["uml"] = uml
            brain.knowledge_base["architecture"] = architecture
        else:
            return False, f"{red}UML and Architecture Design code blocks not found. Please ensure the input data contains both properly formatted code blocks.{reset}"

        # Get the SoftwareDesignJudge module
        judge_module = brain.get_module_by_name("SoftwareDesignJudge")
        judge_module.build_prompt_builder(brain=brain)
        print(f"{cyan}SoftwareDesignJudge Input: {judge_module.prompt_input}{reset}")
        judge_output = judge_module.process(judge_module.prompt_input)
        print(f"{cyan}SoftwareDesignJudge Output: {judge_output}{reset}")
        passes = SoftwareDesignMilestone.check_for_two_passes(judge_output)
        if passes:
            return True, f"{green}UML and Architecture Design validated and stored in the knowledge base.{reset}"
        else:
            return False, f"{red}UML and Architecture Design failed validation. Please review the output and make necessary corrections.{reset}"


    @staticmethod
    def check_for_two_passes(judges_output: str):
        pass_count = judges_output.count('"pass/fail": "pass"')
        return pass_count > 1


    @staticmethod
    def extract_code_block(text: str) -> str:
        start = text.find("```")
        if start == -1:
            return ""
        end = text.find("```", start + 3)
        return text[start + 3:end].strip() if end != -1 else ""

    @staticmethod
    def find_uml_architecture_start(text: str) -> tuple[int, int]:
        uml_start = text.find("# UML Diagram")
        architecture_start = text.find("# Architecture Design")
        return uml_start, architecture_start

    @staticmethod
    def parse_input_data(_input_data: str) -> tuple[str, str]:
        start_uml, start_arch = SoftwareDesignMilestone.find_uml_architecture_start(_input_data)
        if start_uml == -1 or start_arch == -1:
            return "", ""
        text_uml, text_arc = (
            SoftwareDesignMilestone.extract_code_block(_input_data[start_uml:start_arch]),
            SoftwareDesignMilestone.extract_code_block(_input_data[start_arch:])
        )
        return text_uml, text_arc


if __name__ == "__main__":
    milestone = SoftwareDesignMilestone()

