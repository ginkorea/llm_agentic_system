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

if __name__ == "__main__":
    # Set parameters for testing
    brain_type = 'code'  # Options: 'code', 'simple', 'cognitive'
    memory_type = 'cuda'  # Options: 'embedded', 'cuda', 'openvino'
    chaining_mode = True  # Enable chaining mode
    goal = "Develop a Python Package based on the PRD."  # Goal description
    goal_file = 'devbench/benchmark_data/python/lice/PRD.md'

    # Initialize agent
    agent = Agent(
        brain_type=brain_type,
        memory_type=memory_type,
        chaining=chaining_mode,
        goal=goal,
        goal_file=goal_file
    )

    # Run the agent
    agent.run()
