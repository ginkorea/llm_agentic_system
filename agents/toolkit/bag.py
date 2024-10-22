from agents.toolkit.search import search
from agents.toolkit.get_page import get_page
from agents.toolkit.calculate import calculate
from agents.toolkit.visualize_file_structure import visualize_file_structure

from langchain_core.tools.structured import \
    StructuredTool  # Importing StructuredTool to use as a type for structured tools


class BagOfTools:
    """A class to manage various tools, such as search, get_page, calculate, and visualize_file_structure."""

    def __init__(self, verbose: bool = True):
        """Initialize the BagOfTools class with optional verbosity."""
        self.verbose = verbose  # Whether to print detailed information
        self.tools = []  # List to hold all structured tools
        self.search = search  # Search tool
        self.get_page = get_page  # Tool to get a web page's content
        self.calculate = calculate  # Tool to evaluate mathematical expressions
        self.visualize_file_structure = visualize_file_structure  # Tool to visualize file structures
        self.bind_tools()  # Automatically bind all tools

    def bind_tools(self):
        """Bind tools dynamically by checking for StructuredTool instances."""
        for attr_name in dir(self):  # Loop through attributes of the instance
            if not attr_name.startswith('_'):  # Ignore private methods/attributes
                attr_value = getattr(self, attr_name)  # Get attribute value
                if isinstance(attr_value, StructuredTool):  # If the attribute is a StructuredTool instance
                    if self.verbose:
                        print(f"Adding {attr_name} to tools")
                    self.tools.append(attr_value)  # Add the tool to the tools list
                else:
                    if self.verbose:
                        print(f"Skipping {attr_name}, not a StructuredTool instance")

    def get_tools(self):
        """Returns the list of all tools, printing their names if verbose is enabled."""
        if self.verbose:
            print("Available tools:")
        for _tool in self.tools:  # Print all tools with their descriptions
            if self.verbose:
                print(f"--{_tool.name}: {_tool.description}")
        return self.tools
