from agents.toolkit.search import search
from agents.toolkit.get_page import get_page
from agents.toolkit.calculate import calculate
from agents.toolkit.to_upper import to_upper
from agents.toolkit.visualize_file_structure import visualize_file_structure  # Import the new tool

class BagOfTools:
    def __init__(self):
        self.tools = []
        self.bind_tools()
        self.search = search
        self.get_page = get_page
        self.calculate = calculate
        self.to_upper = to_upper
        self.visualize_file_structure = visualize_file_structure  # Add the new tool

    def bind_tools(self):
        """Method to bind all tool methods inside the BagOfTools."""
        for name, method in self.__class__.__dict__.items():
            if callable(method) and hasattr(getattr(self, name), "as_tool"):
                structured_tool = getattr(self, name).as_tool()
                desc = structured_tool.description.split(".")[0]
                self.tools.append({"name": name, "desc": desc, "tool": getattr(self, name)})

    def get_tools(self, verbose: bool = True):
        """Returns the list of all tools."""
        if verbose:
            print("Available tools:")
        for _tool in self.tools:
            if verbose:
                print(f"--{_tool['name']}: {_tool['desc'][23:]}")
        return self.tools
