from typing import Optional

from agents.brain.lobes.module import Module
from agents.brain.prompts.structured.controller_prompt import ControllerPrompt
from agents.brain.prompts.structured.get_goal_from_file_prompt import GoalBuilderPrompt
from agents.brain.core import Brain
from agents.brain.prompts.examples.code_examples import CodeExamples












# LogicLobe: Code logic structuring and algorithm development
class LogicLobe(Module):
    """Responsible for code logic structuring and algorithm development."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=10,
            system_message="You develop code logic, ensuring efficient algorithms and clear structure."
        )


# DebuggerLobe: Initial debugging and error resolution
class DebuggerLobe(Module):
    """Specializes in identifying, explaining, and resolving common code errors."""

    def __init__(self):
        super().__init__(
            model_name="o1-mini",  # Suitable for quick debugging tasks
            temperature=1,
            memory_limit=7,
            system_message=None,  # System message not supported in o1-mini
            alt_system_message="You identify, explain, and resolve common code errors using advanced reasoning."
        )


# SeniorDev: Escalation module for complex debugging
class SeniorDev(Module):
    """Handles complex code debugging and problem-solving, serving as the escalation point for challenging issues."""

    def __init__(self):
        super().__init__(
            model_name="o1-preview",  # Enhanced reasoning capabilities
            temperature=1, # o1-preview only supports temperature=1
            memory_limit=15,
            system_message=None,  # System message not supported in o1-preview
            alt_system_message="You handle complex code debugging and problem-solving, serving as the escalation point for challenging issues."
        )


# SyntaxLobe: Syntax and boilerplate code generation
class SyntaxLobe(Module):
    """Focuses on generating correct syntax, boilerplate code, and structure."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.2,
            memory_limit=5,
            system_message="You generate correct syntax and structure, focusing on language-specific requirements."
        )


# DocumentationLobe: Code commenting and documentation
class DocumentationLobe(Module):
    """Generates comments and documentation for code explanation."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.4,
            memory_limit=3,
            system_message="You create comments and documentation to explain code functionality."
        )


# TestingLobe: Code testing and unit test generation
class TestingLobe(Module):
    """Generates test cases and unit tests for verifying code functionality."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o-mini",
            temperature=0.3,
            memory_limit=6,
            system_message="You generate test cases and unit tests to ensure code reliability."
        )


# OptimizerLobe: Code optimization and refactoring
class OptimizerLobe(Module):
    """Optimizes code for efficiency and readability."""

    def __init__(self):
        super().__init__(
            model_name="o1-mini",
            temperature=1,
            memory_limit=5,
            system_message=None,  # System message omitted
            alt_system_message="You optimize code for efficiency and readability, enhancing performance and maintainability."
        )


# RefactorLobe: Code refactoring and restructuring
class RefactorLobe(Module):
    """Refactors code to improve clarity, readability, and maintainability."""

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.4,
            memory_limit=8,
            system_message="You refactor code for clarity, readability, and adherence to best practices."
        )


if __name__ == "__main__":
    # Example test of DebuggerLobe and SeniorDev instances


    manager = TaskRouter()
    debugger = DebuggerLobe()
    senior_dev = SeniorDev()

    print("Manager Function Info:")
    print(manager.get_info())

    print("Debugger Info:")
    print(debugger.get_info())

    print("SeniorDev Info:")
    print(senior_dev.get_info())

    # Example usage for escalating issues
    error_message = "Why is this function throwing a TypeError?"

    # Manager directs the task to DebuggerLobe first
    result = debugger.process([{"role": "user", "content": error_message}])
    print("Debugger Result:", result)

    # Escalate to SeniorDev if the issue persists
    if "unresolved" in result.lower():  # Hypothetical check for unresolved issues
        result = senior_dev.process([{"role": "user", "content": error_message}])
        print("SeniorDev Result:", result)
