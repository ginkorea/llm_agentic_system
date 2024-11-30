import argparse
import logging
from agents.base import Agent


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

if __name__ == "__main__":
    # Parse arguments
    args = parse_arguments()

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
