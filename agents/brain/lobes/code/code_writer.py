# code_writer.py

from agents.brain.lobes.module import Module
from agents.brain.prompts.examples.code_writer_examples import CodeWriterExamples
from agents.brain.prompts.structured.code_writer_prompt import CodeWriterPrompt

class CodeWriter(Module):
    """
    Handles the code generation phase, producing Python files based on PRD, UML Diagram, and Architecture Design.
    """

    def __init__(self):
        super().__init__(
            model_name="gpt-4o",
            temperature=0.5,
            memory_limit=10,
            system_message="Analyze the PRD, UML Diagram, Architecture Design, Required Classes, and Existing Code Base "
                           " to generate Python code files.",
        )
        self.examples = CodeWriterExamples()
        self.prompt_builder = None

    def build_prompt_builder(self, brain=None, modules=None, tools=None, examples=None, **kwargs):
        """
        Initializes the prompt builder using the CodeWriterPrompt class.
        """
        examples = self.examples.get_examples() if examples is None else examples
        prd, uml_class, uml_sequence, architecture = (brain.knowledge_base.get("prd", ""),
                                                      brain.knowledge_base.get("uml_class", ""),
                                                      brain.knowledge_base.get("uml_sequence"),
                                                      brain.knowledge_base.get("architecture", ""))
        required_classes = brain.knowledge_base.get("required_classes", "")
        code_base = brain.knowledge_base.get("code", "")
        implemented_classes = code_base.items() if code_base else []
        kwargs.update({
            "required_classes": required_classes,
            "implemented_classes": implemented_classes,
            "prd": prd,
            "uml_class": uml_class,
            "uml_sequence": uml_sequence,
            "architecture": architecture,
            "code_base": code_base
        })
        self.prompt_builder = CodeWriterPrompt(modules=modules, tools=tools, examples=examples, **kwargs)
