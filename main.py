from agents.base import Agent

if __name__ == "__main__":
    # Set parameters for testing
    brain_type = 'code'  # Options: 'code', 'simple', 'cognitive'
    memory_type = 'cuda'  # Options: 'embedded', 'cuda', 'openvino'
    chaining_mode = True  # Set to True to enable chaining mode, False for human interaction mode
    goal = "Complete the UML documentation for the software package for Virus Detection on Fedora Linux"  # Set a goal for chaining mode
    goal_file = 'devbench/benchmark_data/python/lice/PRD.md'  # Set a goal file for chaining mode

    # Initialize agent with the specified brain type and memory type
    agent = Agent(brain_type=brain_type, memory_type=memory_type, chaining=chaining_mode, goal=goal, goal_file=goal_file)


    # Run the agent
    agent.run()
# This script demonstrates how to create an Agent with different brain types and memory types, and run it in either human interaction