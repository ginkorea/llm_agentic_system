from agents.brain.lobes.module import Module
from agents.brain.prompts.examples.acceptance_test_examples import AcceptanceTestExamples
from agents.brain.prompts.structured.acceptance_test_prompt import AcceptanceTestPrompt


class AcceptanceTestGenerator(Module):
    """
    Generates acceptance tests based on PRD, UML Diagram, and Architecture Design.
    """

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=5,
            system_message="Analyze the PRD, UML Diagram, and Architecture Design to generate acceptance tests.",
        )
        self.examples = AcceptanceTestExamples()
        self.prompt_builder = None

    def build_prompt_builder(self, brain=None, modules=None, tools=None, examples=None, **kwargs):
        """
        Initializes the prompt builder using the AcceptanceTestPrompt class.
        """
        examples = self.examples.get_examples() if examples is None else examples
        prd = brain.knowledge_base.get("prd", "")
        uml_class = brain.knowledge_base.get("uml_class", "")
        architecture = brain.knowledge_base.get("architecture", "")
        code_files = brain.knowledge_base.get("code", {})

        kwargs.update({
            "prd": prd,
            "uml_class": uml_class,
            "architecture": architecture,
            "code_files": code_files,
        })
        self.prompt_builder = AcceptanceTestPrompt(modules=modules, tools=tools, examples=examples, **kwargs)


