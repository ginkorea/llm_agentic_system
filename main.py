from agents.base import Agent


if __name__ == "__main__":

    agent = Agent(brain_type='code', memory_type='cuda') # defaults to embedded memory, but can be changed to 'cuda' or 'openvino' for acceleration
    agent.run()

## to change the brain_type use simple or cognitive
## to change the memory_type use embedded, cuda or openvino

