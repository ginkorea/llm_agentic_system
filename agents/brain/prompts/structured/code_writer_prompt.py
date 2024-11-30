# code_writer_prompt.py

from agents.brain.prompts.structured.structured_prompt import StructuredPrompt
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from agents.brain.core import Brain  # Import only for type checking

class CodeWriterPrompt(StructuredPrompt):
    """
    Specialized prompt for generating Python files based on PRD, UML Diagram, and Architecture Design.
    """

    def __init__(self, tools=None, modules=None, examples=None, goal=None):
        super().__init__(tools=tools, modules=modules, examples=examples, goal=goal)
        self.base_prompt = """
        You are a code generation expert. Your task is to analyze the PRD, UML Class and Sequence Diagrams, and Architecture Design to generate:
        - One Python file per class described in the UML Class Diagram.
        - A `main.py` file integrating all classes.

        Each output should be a properly formatted Python code block with the filename as a comment at the top.
        
        for example the main.py file should look like this:
        ```python
        # main.py
        import class1
        import class2
        import class3
        
        if __name__ == "__main__":
        # your code here ...
        ```
        
        generate one code block per class and one for the main.py file.
        """

    def build_prompt(self, brain: 'Brain', prompt_input: str, previous_output: bool = False,
                     previous_module: Optional[str] = None, goal=None, **kwargs) -> str:
        """
        Builds the prompt for generating Python code files.

        Parameters:
        - prompt_input: Input text combining PRD, UML, and Architecture Design.
        """
        self.reset_prompt(goal=goal)
        self.prompt += f"""
        {self.base_prompt}

        Examples:
        ----------------
        {self.examples}

        ----------------
        
        The examples above are for reference only. Your code should be based on the provided input below.
        Analyze the following PRD, UML Diagram, and Architecture Design to generate Python code files:

        Input:
        ----------------
        
        Prompt Input:
        {prompt_input}
                
        PRD: 
        {brain.knowledge_base.get("prd", "PRD not found")}    
        
        UML Class Diagram:
        {brain.knowledge_base.get("uml_class", "UML Class Diagram not found")}
        
        UML Sequence Diagram:
        {brain.knowledge_base.get("uml_sequence", "UML Sequence Diagram not found")}
        
        Architecture Design:
        {brain.knowledge_base.get("architecture", "Architecture Design not found")}

        Implement the Following Required Classes:
        ----------------
        {brain.knowledge_base.get("required_classes", "No required classes found.")}
        ----------------
        
        The following classes are already implemented in the code base below:
        ----------------
        {brain.knowledge_base.get("implemented_classes", "No implemented classes found.")}
        ----------------
        
        Existing Code Base:
        ----------------
        {brain.knowledge_base.get("code", "No existing code base found.")}
        
        ----------------
                
        Generate the Python code files as described above, one code block per class and one for the `main.py` file  
        Ensure that you add any folder or module nesting as well as '__init__.py' to make the modules works.  
        All modules should be prefixed with the "workbench" module name.  for instance if the module is myproject, the module should be workbench.myproject.
        Do not prefix filenames with "workbench.".
        """
        return self.prompt
