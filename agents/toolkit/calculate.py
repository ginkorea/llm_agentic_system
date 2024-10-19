from typing import Any

from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str | Any:
    """Calculate the result of a mathematical expression."""
    try:
        return eval(expression)
    except Exception as e:
        return f"Error: {e}"


