from agents.brain.lobes.module import Module
from agents.brain.prompts.examples.unit_test_examples import UnitTestExamples
from agents.brain.prompts.structured.unit_test_prompt import UnitTestPrompt


class UnitTestGenerator(Module):
    """
    Generates unit tests for individual components of the codebase.
    """

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=5,
            system_message="Generate unit tests for Python code based on PRD, UML Diagram, and Architecture Design.",
        )
        self.examples = UnitTestExamples()
        self.prompt_builder = None

    def build_prompt_builder(self, brain=None, modules=None, tools=None, examples=None, **kwargs):
        """
        Initializes the prompt builder using the UnitTestPrompt class.
        """
        examples = self.examples.get_examples() if examples is None else examples
        prd = brain.knowledge_base.get("prd", "")
        uml_class = brain.knowledge_base.get("uml_class", "")
        code_files = brain.knowledge_base.get("code", {})

        kwargs.update({
            "prd": prd,
            "uml_class": uml_class,
            "code_files": code_files,
        })
        self.prompt_builder = UnitTestPrompt(modules=modules, tools=tools, examples=examples, **kwargs)

