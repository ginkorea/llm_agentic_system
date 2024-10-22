# Toolkit Submodule

## Overview

The **Toolkit submodule** provides a set of tools that enhance the capabilities of the **autonomous software development system**. These tools enable the system to perform specialized tasks such as searching, scraping web pages, performing calculations, and visualizing file structures. 

The tools are dynamically managed by the **`BagOfTools`** class, which handles the integration and binding of each tool into the overall system. This modular design allows the toolkit to be easily extended and customized for future needs.

<img src="toolkit_module_image.png" width="800" alt="Toolkit Module Image">

### LangChain Integration

Each tool inherits from the **LangChain Core's `StructuredTool`** class, making them compatible with the LangChain framework for managing tool execution. This allows the autonomous agent to invoke these tools dynamically based on the needs of the task.

### Core Tools

The toolkit contains the following core tools:

1. **`calculate`**: 
   - Evaluates mathematical expressions using Python’s `eval` function.
   - Example usage: `calculate("2 + 2")` returns `4`.

2. **`get_page`**:
   - Retrieves the full text of a web page using a headless browser with Selenium.
   - Example usage: `get_page("https://example.com")` returns the page content.

3. **`search`**:
   - Performs a web search using Google’s JSON API and returns top results as a list of dictionaries.
   - Example usage: `search({"query": "Python programming", "n_sites": 3})` returns top search results.

4. **`visualize_file_structure`**:
   - Recursively builds a graph and text-based tree of the file structure, using colored submodules.
   - Outputs both a PDF graph and a text file of the structure.

### BagOfTools Class

The **`BagOfTools`** class is responsible for managing and binding tools dynamically. It automatically detects tools that are instances of `StructuredTool` and makes them available for the agent to use.

- **`bind_tools`**: Automatically binds tools that inherit from LangChain's `StructuredTool` class to the agent's toolkit.
- **`get_tools`**: Returns a list of all available tools with optional verbose logging to describe each tool’s functionality.

```python
from agents.toolkit.bag import BagOfTools

toolkit = BagOfTools(verbose=True)
toolkit.get_tools()  # Displays and returns all available tools
```

### Adding New Tools

To add new tools to the toolkit, follow these steps:

1. **Create the tool**:
   Each tool must be a function decorated with the `@tool` decorator from LangChain Core.

   Example of a new tool:
   ```python
   from langchain_core.tools import tool

   @tool
   def to_upper(text: str) -> str:
       """Converts a string to uppercase."""
       return text.upper()
   ```

2. **Add the tool to `BagOfTools`**:
   Once the tool is created, it will automatically be detected by the `BagOfTools` class when `bind_tools` is called. There is no need to manually register the tool, as long as it’s implemented correctly.

### Extensibility

The toolkit is designed to be easily extensible. New tools can be added dynamically, and the agent can invoke any tool based on the task at hand. By utilizing LangChain’s `StructuredTool` class, these tools can be seamlessly integrated into the decision-making process of the autonomous agent.

### Example Usage

Here’s a simple example of how the agent interacts with the toolkit:

```python
from agents.toolkit.bag import BagOfTools

# Initialize the toolkit with verbose output
toolkit = BagOfTools(verbose=True)

# Access and use individual tools
result = toolkit.calculate("5 * 10")
print(f"Calculation Result: {result}")

# Visualize the current file structure
structure = toolkit.visualize_file_structure(start_path=".")
print(structure)
```

### Future Expansion

The **Toolkit submodule** will be expanded significantly with more advanced tools that support additional functionality such as:
- File operations (reading, writing, and editing files).
- API integration for more complex web scraping.
- AI model inference for on-the-fly predictions.

---

This is a starting point for understanding how the Toolkit submodule integrates into the larger system. Stay tuned for more tools and functionality!
```
