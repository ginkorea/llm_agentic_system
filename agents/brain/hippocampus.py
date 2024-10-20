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

    def recall_memory(self, query: str, embedded: bool = True):
        """Search and retrieve memories based on the query."""
        if embedded:
            # Use brain's embedded memory search
            return self.brain.memory.embedding_search(query)
        else:
            # If not using embeddings, search directly from stored text
            return self.brain.memory.search(query)


    def search_memory(self, query: str, embedded: bool = True, long_term: bool = False, top_n: int = 3) -> pd.DataFrame:
        """
        Search memory based on the query. If using embedded memory, it will search based on embeddings.

        Args:
            query (str): The search query.
            embedded (bool): Flag to indicate if we are searching through embedded memory.
            long_term (bool): Flag to indicate if we are searching long-term memory.
            top_n (int): The number of top search results to return.

        Returns:
            pd.DataFrame: The relevant memory entries.
        """
        memory = self.brain.memory

        # If we are using embedded memory, use the embedding search
        if embedded and hasattr(memory, "embedding_search"):
            return memory.search_memory(query, long_term=long_term, top_n=top_n)

        # Fallback to basic string-based search (non-embedded)
        memory_df = memory.long_term_df if long_term else memory.short_term_df
        return memory.tfidf_search(query, long_term=long_term, top_n=top_n)



