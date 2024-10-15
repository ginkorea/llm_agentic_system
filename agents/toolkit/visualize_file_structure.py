import subprocess
from graphviz import Digraph
from langchain_core.tools import tool

@tool
def visualize_file_structure(start_path: str = '.') -> str:
    """Run the `tree` command and generate a graph of the file structure."""
    # Step 1: Run the tree command and capture its output
    try:
        result = subprocess.run(['tree', '-F', '--noreport', start_path], capture_output=True, text=True)
        tree_output = result.stdout
        print(tree_output)
    except Exception as e:
        return f"Error running tree command: {str(e)}"

    # Step 2: Initialize Graphviz object with better formatting options
    dot = Digraph(comment='File Structure')
    dot.attr(size='10,10')  # Set the size of the output graph
    dot.attr(rankdir='TB')  # Top-to-bottom layout
    dot.attr(nodesep='0.5')  # Set the node separation (horizontal spacing)
    dot.attr(ranksep='0.75')  # Set the rank separation (vertical spacing)

    stack = [start_path]  # Initialize the stack with the root directory
    subgraphs = {}  # To keep track of subgraphs (modules)

    # Step 3: Parse the tree command output to create the graph
    for line in tree_output.splitlines():
        indent_level = (len(line) - len(line.lstrip())) // 4  # Count indentation levels
        node_name = line.strip()

        # Remove trailing slashes for files or directories from tree output
        clean_node_name = node_name.rstrip('/')

        # Pop the stack if we're going up in directory levels
        while len(stack) > indent_level + 1:
            stack.pop()

        # Determine the parent (current top of the stack)
        parent = stack[-1] if stack else None

        # Add directories as subgraphs (modules)
        if node_name.endswith('/'):  # Directory
            # Check if we are entering a new module
            if indent_level == 0 or parent not in subgraphs:
                subgraph = Digraph(name=f'cluster_{clean_node_name}')
                subgraph.attr(label=clean_node_name, style='filled', color='lightgrey')  # Label and style for modules
                subgraphs[clean_node_name] = subgraph
            stack.append(clean_node_name)  # Add directory to the stack
        else:  # File
            if parent:
                subgraph = subgraphs.get(parent, dot)  # Add files to the correct module (or main graph)
                subgraph.node(clean_node_name, shape='note')
                subgraph.edge(parent, clean_node_name)

    # Add subgraphs to the main graph
    for subgraph in subgraphs.values():
        dot.subgraph(subgraph)

    # Save and render the graph
    output_file = 'file_structure_graph'
    dot.render(output_file, view=False)  # Generates a PDF file

    return f"File structure graph generated as {output_file}.pdf"
