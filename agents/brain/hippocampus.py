from agents.brain.lobes import Lobe
import pandas as pd


class Hippocampus(Lobe):
    def __init__(self, brain):
        super().__init__(
            memory_limit=10,
            system_message="You are responsible for recalling long-term memory and maintaining continuity.",
            initialize_model=False  # Prevents OpenAI model initialization
        )
        self.brain = brain  # Access the brain's memory for retrieval
        self.embedded = self.brain.memory.embedded

    def recall_memory(self, query: str):
        """Search and retrieve memories based on the query."""
        if self.embedded:
            # Use brain's embedded memory search
            return self.brain.memory.embedding_search(query)
        else:
            # If not using embeddings, search directly from stored text
            return self.brain.memory.search(query)

    def process(self, user_input: str, memory: pd.DataFrame = None) -> pd.DataFrame:
        """
        Processes the refined prompt, extracts the relevant memory search instructions,
        and returns the corresponding memories.

        Args:
            :param memory: The memory data (short-term or long-term) to be used for retrieval.
            :param user_input:  (str): A semicolon-separated refined prompt in the format [top_n; memory_type; search_query].
        Returns:
            pd.DataFrame: The retrieved memories.

        """

        # Remove the square brackets and split the prompt by semicolons
        print("user_input", user_input)
        refined_prompt = user_input.strip()[1:-1]  # Remove the brackets
        print("refined_prompt", refined_prompt)
        parts = [part.strip() for part in refined_prompt.split(';')]
        print("parts", parts)

        if len(parts) != 3:
            print("Refined prompt must be in the format '[top_n; memory_type; search_query]'.")
            print(parts)
            raise ValueError("Refined prompt must be in the format '[top_n; memory_type; search_query]'.")
            #TODO make this rerun the prompt using the prefrontal cortex, provided the error message to the LLM


        # Extract the components from the refined prompt
        try:
            top_n = int(parts[0])
        except ValueError:
            top_n = 3 # Default to top 3 if parsing fails (or not provided)
            if top_n > len(memory):
                top_n = len(memory)

        memory_type = parts[1]
        search_query = parts[2]

        # Determine the correct memory to search
        if memory_type.count("long") > 0:
            memory_df = self.brain.memory.long_term_df  # Assuming you have long_term_df
        else:
            memory_df = self.brain.memory.short_term_df

        # Perform the memory search using the parsed components
        if self.brain.verbose:
            print("search_query", search_query)
            print("top_n", top_n)
            print("searching memory for query")

        return self.brain.memory.embedding_search(query=search_query, memory_df=memory_df, top_n=top_n)

