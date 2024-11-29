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
        uml_class, uml_sequence, architecture = SoftwareDesignMilestone.parse_input_data(_input_data)
        if uml_class and uml_sequence and architecture:
            brain.knowledge_base["uml_class"] = uml_class
            brain.knowledge_base["uml_sequence"] = uml_sequence
            brain.knowledge_base["architecture"] = architecture
        else:
            return False, f"{red}UML Class, UML Sequence, and Architecture Design code blocks not found or incomplete. Please ensure the input data contains all three properly formatted code blocks.{reset}"

        # Get the SoftwareDesignJudge module
        judge_module = brain.get_module_by_name("SoftwareDesignJudge")
        judge_module.build_prompt_builder(brain=brain)
        print(f"{cyan}SoftwareDesignJudge Input: {judge_module.prompt_input}{reset}")
        judge_output = judge_module.process(judge_module.prompt_input)
        print(f"{cyan}SoftwareDesignJudge Output: {judge_output}{reset}")
        passes = SoftwareDesignMilestone.check_for_two_passes(judge_output)
        if passes:
            SoftwareDesignMilestone.dump_files(brain)
            return True, f"{green}UML and Architecture Design validated and stored in the knowledge base.{reset}"
        else:
            return False, f"{red}UML and Architecture Design failed validation. Please review the output and make necessary corrections.{reset}"

    @staticmethod
    def check_for_two_passes(judges_output: str):
        pass_count = judges_output.count('"pass/fail": "pass"')
        return pass_count > 2

    @staticmethod
    def save_file(file_name: str, data: str):
        with open(file_name, "w") as file:
            file.write(data)

    @staticmethod
    def dump_files(brain):
        uml_class = brain.knowledge_base.get("uml_class", "")
        uml_sequence = brain.knowledge_base.get("uml_sequence", "")
        architecture = brain.knowledge_base.get("architecture", "")
        if uml_class:
            SoftwareDesignMilestone.save_file("uml_class.md", uml_class)
        if uml_sequence:
            SoftwareDesignMilestone.save_file("uml_sequence.md", uml_sequence)
        if architecture:
            SoftwareDesignMilestone.save_file("architecture.md", architecture)

    @staticmethod
    def extract_code_block(text: str) -> str:
        start = text.find("```")
        if start == -1:
            return ""
        end = text.find("```", start + 3)
        return text[start + 3:end].strip() if end != -1 else ""

    @staticmethod
    def find_component_start(text: str) -> tuple[int, int, int]:
        uml_class_start = text.find("# UML Class Diagram")
        uml_sequence_start = text.find("# UML Sequence Diagram")
        architecture_start = text.find("# Architecture Design")
        return uml_class_start, uml_sequence_start, architecture_start

    @staticmethod
    def parse_input_data(_input_data: str) -> tuple[str, str, str]:
        start_class, start_sequence, start_arch = SoftwareDesignMilestone.find_component_start(_input_data)
        if start_class == -1 or start_sequence == -1 or start_arch == -1:
            return "", "", ""
        uml_class = SoftwareDesignMilestone.extract_code_block(_input_data[start_class:start_sequence])
        uml_sequence = SoftwareDesignMilestone.extract_code_block(_input_data[start_sequence:start_arch])
        architecture = SoftwareDesignMilestone.extract_code_block(_input_data[start_arch:])
        return uml_class, uml_sequence, architecture
