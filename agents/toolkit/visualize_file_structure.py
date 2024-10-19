import os
from graphviz import Digraph
from langchain_core.tools import tool

# A list of colors to cycle through for submodules (directories)
COLORS = ['lightblue', 'lightgreen', 'yellow', 'pink', 'lightgrey', 'lightcyan', 'orange']

def get_color(index):
    """Return a color from the COLORS list based on the index."""
    return COLORS[index % len(COLORS)]

def save_graph(dot, output_file):
    """Save and render the graph to a PDF file."""
    dot.render(output_file, view=False)  # Generates a PDF file
    return f"File structure graph generated as {output_file}.pdf"

def save_text_output(text_output, text_output_file):
    """Save the text output to a file."""
    with open(text_output_file, 'w') as f:
        f.write(text_output)
    return f"Text-based tree saved as {text_output_file}"

def should_ignore(item):
    """Returns True if the directory or file should be ignored."""
    # Ignore __pycache__ and hidden files/directories
    return item.startswith('.') or item == '__pycache__' or item == 'devbench'

def add_nodes(dot, path, parent=None, indent="", color_index=0, text_output=""):
    """Recursively add directories and files to the graph and text-based output."""
    # Get the current directory's content, ignore hidden files and directories to be ignored
    if path == "":
        path = "."
    try:
        os.listdir(path)
    except PermissionError:
        return text_output
    except FileNotFoundError:
        return text_output
    for item in sorted(os.listdir(path)):
        if should_ignore(item):
            continue  # Skip ignored files and directories

        item_path = os.path.join(path, item)

        # Directory handling
        if os.path.isdir(item_path):
            # Add the directory as a folder node with color
            dot.node(item_path, label=item, shape='folder', style='filled', fillcolor=get_color(color_index))
            if parent:
                # Connect the directory to its parent
                dot.edge(parent, item_path)

            # Add directory to text output
            text_output += f"{indent}{item}/\n"

            # Recursively add the directory's contents (increase indentation and color index)
            text_output = add_nodes(dot, item_path, item_path, indent + "    ", color_index + 1, text_output)

        # File handling
        else:
            # Add file as a note node
            dot.node(item_path, label=item, shape='note')
            if parent:
                # Connect the file to its parent directory
                dot.edge(parent, item_path)

            # Add file to text output
            text_output += f"{indent}{item}\n"

    return text_output

@tool
def visualize_file_structure(start_path: str = '.') -> str:
    """Recursively build a graph and a text-based tree of the file structure with colored submodules."""
    # Initialize Graphviz object with formatting options
    dot = Digraph(comment='File Structure')
    dot.attr(size='10,10')  # Set the size of the output graph
    dot.attr(rankdir='TB')  # Top-to-bottom layout
    dot.attr(nodesep='0.5')  # Set the node separation (horizontal spacing)
    dot.attr(ranksep='0.75')  # Set the rank separation (vertical spacing)

    # Start the recursion from the root directory
    text_output = add_nodes(dot, start_path)

    output_dir = 'home/gompert/workspace/llmas/agents/brain/memory/file_structure/' # Output directory for the generated files

    # Save and render the graph as PDF
    output_file = output_dir + 'graph'
    graph_message = save_graph(dot, output_file)

    # Save the text output to a file
    text_output_file = output_dir + 'tree.txt'
    text_message = save_text_output(text_output, text_output_file)

    return f"{graph_message} and {text_message}"
