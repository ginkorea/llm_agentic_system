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
        uml_class, uml_sequence, architecture = self.parse_input_data(_input_data)

        # Retrieve the SoftwareDesignJudge module
        judge_module = brain.get_module_by_name("SoftwareDesignJudge")
        results = []

        if uml_class:
            result = judge_module.validate_uml_class(uml_class, brain.knowledge_base.get("required_classes", set()))
            if result[0]:  # Save if validation passes
                brain.knowledge_base["uml_class"] = uml_class
                self.save_file("uml_class.uml", uml_class)
            results.append(("UML Class Diagram", result))
        else:
            results.append(("UML Class Diagram", (False, "UML Class Diagram is missing or incomplete.")))

        if uml_sequence:
            result = judge_module.validate_uml_sequence(uml_sequence)
            if result[0]:  # Save if validation passes
                brain.knowledge_base["uml_sequence"] = uml_sequence
                self.save_file("uml_sequence.uml", uml_sequence)
            results.append(("UML Sequence Diagram", result))
        else:
            results.append(("UML Sequence Diagram", (False, "UML Sequence Diagram is missing or incomplete.")))

        if architecture:
            result = judge_module.validate_architecture(architecture)
            if result[0]:  # Save if validation passes
                brain.knowledge_base["architecture"] = architecture
                self.save_file("architecture.md", architecture)
            results.append(("Architecture Design", result))
        else:
            results.append(("Architecture Design", (False, "Architecture Design is missing or incomplete.")))

        # Check if all components passed
        all_passed = all(result[1][0] for result in results)
        if all_passed:
            return True, f"{green}UML and Architecture Design validated and stored in the knowledge base.{reset}"

        # Create a detailed failure report
        failure_details = "\n".join(
            f"{red}{name}: {result[1][1]}{reset}" for name, result in results if not result[1][0]
        )
        return False, f"{red}UML and Architecture Design failed validation. Details:\n{failure_details}{reset}"

    @staticmethod
    def save_file(file_name: str, data: str):
        with open(file_name, "w") as file:
            file.write(data)

    @staticmethod
    def extract_code_block(text: str) -> str:
        start = text.find("```")
        if start == -1:
            return ""
        end = text.find("```", start + 3)
        return text[start + 3:end].strip() if end != -1 else ""

    @staticmethod
    def parse_input_data(_input_data: str) -> tuple[str, str, str]:
        uml_class_start = _input_data.find("# UML Class Diagram")
        uml_sequence_start = _input_data.find("# UML Sequence Diagram")
        architecture_start = _input_data.find("# Architecture Design")

        uml_class_end = uml_sequence_start if uml_sequence_start != -1 else architecture_start
        uml_sequence_end = architecture_start if architecture_start != -1 else len(_input_data)
        architecture_end = len(_input_data)

        uml_class = _input_data[uml_class_start:uml_class_end].strip() if uml_class_start != -1 else ""
        uml_sequence = _input_data[uml_sequence_start:uml_sequence_end].strip() if uml_sequence_start != -1 else ""
        architecture = _input_data[architecture_start:architecture_end].strip() if architecture_start != -1 else ""

        return (
            SoftwareDesignMilestone.extract_code_block(uml_class),
            SoftwareDesignMilestone.extract_code_block(uml_sequence),
            SoftwareDesignMilestone.extract_code_block(architecture),
        )
