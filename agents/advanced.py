from agents.base import Agent
from langchain.prompts import ChatPromptTemplate
from agents.brain.core import Brain

# BrainAgent class inheriting from Agent
class AdvancedAgent(Agent):
    def __init__(self):
        super().__init__()  # Call the base class constructor
        self.tool_descriptions = None
        self.brain = Brain()  # Use the advanced brain model


    def choose_lobe(self, reasoning: bool):
        """
        Choose the lobe based on the task complexity.
        If reasoning is required, use the frontal lobe; otherwise, use the occipital lobe.
        """
        if reasoning:
            return self.brain.frontal_lobe
        else:
            return self.brain.occipital_lobe

    def determine_action(self, user_input: str, advanced: bool) -> str:
        """
        In AdvancedAgent, determine whether to use a tool or LLM.
        If advanced is True, the LLM will help decide whether to use a tool or generate a response.
        """
        if not advanced:
            # Use the basic logic to choose a tool or LLM
            for tool in self.toolkit.tools:
                if tool.__name__ in user_input:
                    # Extract the part of the input relevant to the tool and execute the tool function
                    expression = user_input.replace(tool.__name__, "").strip()
                    return "tool"

            return "llm"  # If no tool matched, use the LLM

        # Advanced mode: ask the LLM whether to use a tool or generate a response
        tool_info = "\n".join([f"{tool}: {desc}" for tool, desc in self.tool_descriptions.items()])
        prompt = f"""
        You are an intelligent agent with the following tools at your disposal:
        {tool_info}

        Based on the following user input, determine whether the input is best handled by one of the tools or by generating a direct response using the LLM.

        User input: {user_input}
        """
        # Use LLM to decide whether to use a tool or LLM response
        lobe = self.occipital_lobe  # Use a simpler model to save resources
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an agent responsible for choosing tools or using an LLM response."),
            ("user", "{user_input}")
        ])
        chain = prompt_template | lobe
        response = chain.invoke({"user_input": prompt})

        return response.content.strip().lower()  # Return the decision ('tool' or 'llm')

    def process_input(self, user_input: str, reasoning: bool = False) -> str:
        """
        Process the input by deciding whether to throw a tool or use a model.
        """
        # Determine action: advanced decision-making or simple logic
        action = self.determine_action(user_input, reasoning)

        if action == "tool":
            for tool in self.tools:
                if tool.__name__ in user_input:
                    # Extract the part of the input relevant to the tool and execute the tool function
                    expression = user_input.replace(tool.__name__, "").strip()
                    return tool(expression)

        # If LLM is chosen or no tool matched, use the LLM to respond
        lobe = self.choose_lobe(reasoning)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("user", "{user_input}")
        ])
        chain = prompt_template | lobe
        response = chain.invoke({"user_input": user_input})

        # Store memory of the interaction
        self.store_memory(user_input, response.content)

        return response.content
