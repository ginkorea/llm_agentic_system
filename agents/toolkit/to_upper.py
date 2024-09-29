from langchain_core.tools import tool

@tool
def to_upper(input_string: str) -> str:
    """Convert a string to uppercase."""
    return input_string.upper()