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
            return self.brain.memory.embedding_search(query)
        else:
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
        max_retries = 5
        retry_count = 0

        while retry_count < max_retries:
            try:
                print(f"Processing input: {user_input}")

                # Remove the square brackets and split the prompt by semicolons
                refined_prompt = user_input.strip()[1:-1]  # Remove the brackets
                parts = [part.strip() for part in refined_prompt.split(';')]

                if len(parts) != 3:
                    raise ValueError(
                        "Prompt format is incorrect. Expected format is '[top_n; memory_type; search_query]'.")

                # Extract the components from the refined prompt
                try:
                    top_n = int(parts[0])
                except ValueError:
                    raise ValueError(f"Failed to parse '{parts[0]}' as an integer for top_n.")

                memory_type = parts[1].lower()
                search_query = parts[2]

                # Determine the correct memory to search
                if memory_type not in ["long-term", "short-term"]:
                    raise ValueError(
                        f"Invalid memory type: '{memory_type}'. Choose either 'long-term' or 'short-term'.")

                memory_df = self.brain.memory.long_term_df if memory_type == "long-term" else self.brain.memory.short_term_df

                # Perform the memory search using the parsed components
                if self.brain.verbose:
                    print(f"Searching for '{search_query}' in {memory_type} memory, returning top {top_n} results.")

                return self.brain.memory.embedding_search(query=search_query, memory_df=memory_df, top_n=top_n)

            except ValueError as e:
                retry_count += 1
                print(
                    f"Error: {str(e)}. Attempting refinement with PreFrontalCortex. (Retry {retry_count}/{max_retries})")

                # Use PreFrontalCortex to refine the prompt and pass the memory
                prefrontal_cortex = self.brain.get_lobe_by_name("PreFrontalCortex")
                if prefrontal_cortex:
                    # Pass both user_input and memory to the process
                    user_input = prefrontal_cortex.process(f"Error: {str(e)}. Please refine the prompt.", memory)
                else:
                    print("PreFrontalCortex is not available. Exiting.")
                    return pd.DataFrame()  # Return empty DataFrame if no valid prompt is generated

            if retry_count == max_retries:
                # Final fallback after max retries
                return pd.DataFrame(
                    {"Error": ["Failed to process the prompt after multiple attempts. Please revise the input."]})

