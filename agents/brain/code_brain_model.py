from agents.brain.core import Brain
from agents.brain.lobes.code_lobes import (
    TaskRouter, LogicLobe, DebuggerLobe, SeniorDev, SyntaxLobe,
    DocumentationLobe, TestingLobe, OptimizerLobe, RefactorLobe
)
from agents.brain.prompts.examples.code_examples import CodeExamples

class CodeBrain(Brain):
    def __init__(self, toolkit, forget_threshold: int = 10, verbose: bool = True, memory_type='cuda'):
        super().__init__(toolkit, forget_threshold, verbose, memory_type)

        self.tool_descriptions = self.build_tool_descriptions()


        # Add code-focused lobes to the brain
        self.modules = [
            TaskRouter(),      # Task manager directing to other lobes
            LogicLobe(),            # Responsible for structuring code logic
            DebuggerLobe(),         # Primary debugger for initial error resolution
            SeniorDev(),            # Advanced debugging for complex issues
            SyntaxLobe(),           # Generates syntax and boilerplate code
            DocumentationLobe(),    # Creates documentation and comments
            TestingLobe(),          # Generates tests to verify code functionality
            OptimizerLobe(),        # Optimizes code for efficiency and readability
            RefactorLobe()          # Refactors code to improve clarity and best practices
        ]

        # Pre-generate descriptions for tools and modules
        self.module_descriptions = self.build_module_descriptions(include_routing_module=False)
        self.examples = CodeExamples()
        self.router = self.modules[0]
