def default_prompt_builder(tool_descriptions: str, lobe_descriptions: str, examples: str, user_input: str):
    """
    Build a default prompt for the user to make a decision based on the input.
    """
    return f"""You are responsible for reflexive thinking and quick decision-making.
    Available tools:
    {tool_descriptions}

    Available lobes:
    {lobe_descriptions}

    Based on the user's input, decide whether to use a tool or a lobe to handle the task.

    {examples}

    Please respond in JSON format:
    - If using a tool:
    {{
        "use_tool": true,
        "tool_name": "<tool_name>",
        "refined_prompt": "<refined_prompt_for_tool>"
    }}
    - If using a lobe:
    {{
        "use_tool": false,
        "lobe_index": <lobe_index>,
        "refined_prompt": "<refined_prompt_for_lobe>"
    }}

    User input: "{user_input}"
    """

