import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import Field
import pandas as pd
from torch import NoneType

from agents.brain.memory.simple import SimpleMemory

class EmbeddedMemory(SimpleMemory):
    """Base memory class that provides shared functionality for embedding storage and search."""

    max_embedding_size: int = Field(default=0)  # Track the longest embedding size
    long_term_df: pd.DataFrame = Field(default_factory=lambda: pd.DataFrame(columns=["user_input", "response", "embedding"]))
    short_term_df: pd.DataFrame = Field(default_factory=lambda: pd.DataFrame(columns=["user_input", "response", "embedding"]))

    def _generate_embedding(self, text: str) -> np.ndarray:
        """
        Core embedding generation method, meant to be overwritten by subclasses.
        This is where the actual embedding logic resides (e.g., Jina AI, OpenVINO).
        """
        # Placeholder embedding generation logic
        embedding = np.random.rand(1, 512).astype(np.float32).flatten() # Simulated embedding output
        return embedding

    def store_memory(self, user_input: str, response: str, embedding: NoneType = None) -> None:
        """
        Store memory (short-term and long-term) along with generated embeddings.
        :param embedding: embedding to store in memory, generated from user_input and response text.
        :param user_input: Input provided by the user.
        :param response: System's response to the input.
        """
        combined_text = user_input + " " + response

        # Use generate_and_resize to manage embedding sizes
        embedding = self.generate_and_resize(combined_text)

        # Store the memory using the SimpleMemory method, embedding in the DataFrame
        super().store_memory(user_input, response, embedding)

    def generate_and_resize(self, text: str, regenerating: bool = False) -> np.ndarray:
        """
        Generate the embedding and ensure it matches the current max embedding size.
        If the generated embedding is larger, it adjusts the size accordingly.
        """
        embedding = self._generate_embedding(text)

        # Dynamically adjust the size of the embedding
        if len(embedding) > self.max_embedding_size:
            # Update max_embedding_size and regenerate previous embeddings
            self.max_embedding_size = len(embedding)
            if not regenerating:
                self.regenerate_all_embeddings()

        # Pad if too short
        if len(embedding) < self.max_embedding_size:
            embedding = np.pad(embedding, (0, self.max_embedding_size - len(embedding)))
        elif len(embedding) > self.max_embedding_size:
            embedding = embedding[:self.max_embedding_size]

        return embedding

    def embedding_search(self, query: str, memory_df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
        """Search for top N closest matches based on embeddings."""
        query_embedding = self.generate_and_resize(query)

        embeddings = np.vstack(memory_df['embedding'].values)

        similarities = cosine_similarity([query_embedding], embeddings).flatten()

        top_indices = np.argsort(-similarities)[:top_n]

        return memory_df.iloc[top_indices]

    def search_memory(self, query: str, long_term: bool = False, top_n: int = 3) -> pd.DataFrame:
        """
        Perform an embedding search on the stored memory (short-term or long-term).
        :param query: The search query used to find relevant memories.
        :param long_term: Boolean flag to determine if long-term memory should be searched.
        :param top_n: The number of top search results to return.
        :return: DataFrame of the top N search results based on similarity.
        """
        memory_df = self.long_term_df if long_term else self.short_term_df
        return self.embedding_search(query, memory_df, top_n)


    def regenerate_all_embeddings(self):
        """
        Regenerate embeddings for all previously stored memory entries
        if a larger embedding is encountered, ensuring they are stored
        correctly in a newly created DataFrame.
        """

        def regenerate_embedding(row):
            combined_text = row['user_input'] + " " + row['response']
            embedding = self.generate_and_resize(combined_text, regenerating=True)
            return embedding

        # Create new DataFrames with the same structure
        new_long_term_df = self.long_term_df.copy()
        new_short_term_df = self.short_term_df.copy()

        # Apply embedding regeneration if DataFrames are not empty
        if not new_long_term_df.empty:
            new_long_term_df['embedding'] = new_long_term_df.apply(
                lambda row: regenerate_embedding(row), axis=1)

        if not new_short_term_df.empty:
            new_short_term_df['embedding'] = new_short_term_df.apply(
                lambda row: regenerate_embedding(row), axis=1)

        # Replace the old DataFrames
        self.long_term_df = new_long_term_df
        self.short_term_df = new_short_term_df




