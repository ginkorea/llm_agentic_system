from langchain_core.tools import tool

@tool
def memory_retrieval(agent, memory_type: str = "short_term", print_type: str = "all", rows: int = 5):
    """
    Retrieves memory data from short_term or long_term memory of the agent.

    Args:
        agent: The agent instance containing the memory.
        memory_type (str): Memory type to retrieve ("short_term" or "long_term").
        print_type (str): What to print: "all", "head", or "tail".
        rows (int): Number of rows to display (applicable for head/tail).

    Returns:
        str: The requested memory data as a string.
    """
    if memory_type == "short_term":
        df = agent.memory.short_term_df
    elif memory_type == "long_term":
        df = agent.memory.long_term_df
    else:
        return "Invalid memory type."

    if print_type == "all":
        return df.to_string()
    elif print_type == "head":
        return df.head(rows).to_string()
    elif print_type == "tail":
        return df.tail(rows).to_string()
    else:
        return "Invalid print type."
