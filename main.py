import argparse
import logging
from agents.base import Agent
import os


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Outputs to console
        logging.FileHandler("application.log"),  # Logs to a file
    ]
)

def parse_arguments():
    """
    Parse command-line arguments for the agent configuration.

    Returns:
        Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Run the agent with customizable options.")

    # Add arguments with defaults
    parser.add_argument(
        "--brain_type",
        type=str,
        default="code",
        choices=["code", "simple", "cognitive"],
        help="Type of brain to use (default: 'code')."
    )
    parser.add_argument(
        "--memory_type",
        type=str,
        default="cuda",
        choices=["embedded", "cuda", "openvino"],
        help="Type of memory to use (default: 'cuda')."
    )
    parser.add_argument(
        "--chaining_mode",
        type=bool,
        default=True,
        help="Enable or disable chaining mode (default: True)."
    )
    parser.add_argument(
        "--goal",
        type=str,
        default="Develop a Python Package based on the PRD.",
        help="Goal description for the agent (default: 'Develop a Python Package based on the PRD.')."
    )
    parser.add_argument(
        "--goal_file",
        type=str,
        default="devbench/benchmark_data/python/lice/PRD.md",
        help="Path to the goal file (default: 'devbench/benchmark_data/python/lice/PRD.md')."
    )

    return parser.parse_args()

def clean_space(directory: str = "workbench", add_init: bool = True):
    """
    Clean the workbench directory before running the agent.
    Ensures the directory exists, removes all files and subdirectories,
    and creates a new __init__.py file.

    Args:
        directory (str): Path to the workbench directory (default: "workbench").
        add_init (bool): Add an __init__.py file to the directory (default: True).
    """
    try:
        # Ensure the workbench directory exists
        if not os.path.exists(directory):
            if add_init:
                os.makedirs(directory)

        # Remove all files and subdirectories
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                os.remove(file_path)
            for name in dirs:
                dir_path = os.path.join(root, name)
                os.rmdir(dir_path)

        # Create a new __init__.py file
        if add_init:
            init_file_path = os.path.join(directory, "__init__.py")
            with open(init_file_path, "w") as init_file:
                init_file.write("# Workbench package initialization\n")

        logging.info("Workbench directory cleaned and initialized.")
    except Exception as e:
        logging.error(f"Error cleaning the workbench directory: {e}")


if __name__ == "__main__":
    # Parse arguments
    args = parse_arguments()

    # Clean the workbench and project_env directories
    clean_space()
    clean_space("project_env", add_init=False)

    # Initialize agent with parsed arguments
    agent = Agent(
        brain_type=args.brain_type,
        memory_type=args.memory_type,
        chaining=args.chaining_mode,
        goal=args.goal,
        goal_file=args.goal_file
    )

    # Run the agent
    agent.run()
