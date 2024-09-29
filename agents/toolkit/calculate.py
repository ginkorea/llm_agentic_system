from langchain_core.tools import tool

@tool
def calculate(expression: str) -> float:
    """Calculate the result of a mathematical expression."""
    return eval(expression)


