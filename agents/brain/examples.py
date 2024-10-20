prompt_examples = """
Examples:

User input: "calculate 5 + 5" or "What is 5 + 5?" or "5 + 5" or "calculate: 5 + 5"
Response:
{
    "use_tool": true,
    "tool_name": "calculate",
    "refined_prompt": "5 + 5"
}


User input: "get_page https://www.google.com" or "open https://www.google.com" or "show me https://www.google.com" or "navigate to https://www.google.com"
Response:
{
    "use_tool": true,
    "tool_name": "get_page",
    "refined_prompt": "https://www.google.com"
}

User input: "What is the capital of France?" or "Another easy question: What is the capital of France?"
Response:
{
    "use_tool": false,
    "lobe_index": 0, # PreFrontalCortex
    "refined_prompt": "What is the capital of France?"
}


User input: "Describe the image at the following URL: http://example.com/image.jpg"
Response:
{
    "use_tool": false,
    "lobe_index": 2,
    "refined_prompt": "Describe the image at http://example.com/image.jpg"
}

User input: "Find the top three most relevant memories in your long-term memory related to 'Python'."
Response:
{
    "use_tool": false,
    "lobe_index": -1,
    "refined_prompt": "[3; long-term; Python]"
}
"""