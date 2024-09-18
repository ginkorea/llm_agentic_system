from langchain_core.tools import tool

class BagOfTools:
    def __init__(self):
        self.tools = []
        self.bind_tools()

    @staticmethod
    @tool
    def calculate(expression: str) -> float:
        """Calculate the result of a mathematical expression."""
        return eval(expression)

    @staticmethod
    @tool
    def to_upper(input_string: str) -> str:
        """Convert a string to uppercase."""
        return input_string.upper()

    def bind_tools(self):
        """Method to bind all tool methods inside the BagOfTools."""
        # Use getattr to access the instance-bound methods
        for name, method in self.__class__.__dict__.items():
            if callable(method) and hasattr(getattr(self, name), "as_tool"):
                structured_tool = getattr(self, name).as_tool()
                desc = structured_tool.description.split(".")[0] # Get the first sentence of the description
                desc = desc[23:] # Remove the "unused" part of the description
                self.tools.append({"name": name, "desc": desc, "tool": getattr(self, name)})

    def get_tools(self, verbose: bool = True):
        """Returns the list of all tools."""
        if verbose: print("Available tools:")
        for _tool in self.tools:
            if verbose: print(f"--{_tool['name']}: {_tool['desc']}")
        return self.tools


