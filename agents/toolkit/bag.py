from agents.toolkit.search import search
from agents.toolkit.get_page import get_page
from agents.toolkit.calculate import calculate
from agents.toolkit.to_upper import to_upper
from agents.toolkit.visualize_file_structure import visualize_file_structure

from langchain_core.tools.structured import StructuredTool  # Import StructuredTool

class BagOfTools:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.tools = []
        self.search = search
        self.get_page = get_page
        self.calculate = calculate
        self.to_upper = to_upper
        self.visualize_file_structure = visualize_file_structure
        self.bind_tools()

    def bind_tools(self):
        for attr_name in dir(self):
            if not attr_name.startswith('_'):
                attr_value = getattr(self, attr_name)
                if isinstance(attr_value, StructuredTool):
                    if self.verbose:
                        print(f"Adding {attr_name} to tools")
                    self.tools.append(attr_value)
                else:
                    if self.verbose:
                        print(f"Skipping {attr_name}, not a StructuredTool instance")

    def get_tools(self):
        """Returns the list of all tools."""
        if self.verbose:
            print("Available tools:")
        for _tool in self.tools:
            if self.verbose:
                print(f"--{_tool.name}: {_tool.description}")
        return self.tools
