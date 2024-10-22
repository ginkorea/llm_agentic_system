from typing import Any
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str | Any:
    """Evaluate a mathematical expression and return the result."""
    try:
        # Evaluate the expression using Python's eval function
        return eval(expression)
    except Exception as e:
        # Return the error message if evaluation fails
        return f"Error: {e}"
