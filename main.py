import const.sk as sk
from agents.advanced import AdvancedAgent
from agents.base import Agent
from agents.brain.memory.model.get import get_model_dir

if __name__ == "__main__":

    model_directories = get_model_dir()[0]
    print(model_directories)