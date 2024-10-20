from agents.advanced import AdvancedAgent



if __name__ == "__main__":

    agent = AdvancedAgent(memory_type="cuda") # cuda or openvino for memory_type
    agent.run()



