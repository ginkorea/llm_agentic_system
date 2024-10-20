from agents.base import Agent


if __name__ == "__main__":

    agent = Agent(memory_type="cuda") # cuda or openvino for memory_type
    agent.run()



