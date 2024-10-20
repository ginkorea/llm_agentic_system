import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import Field, PrivateAttr
import pandas as pd
from agents.brain.memory.simple import SimpleMemory

class EmbeddedMemory(SimpleMemory):
    """Base memory class that provides shared functionality for embedding storage and search."""

    embedded: bool = True

    embedding_size: int = 1024  # Adjusted to match model's hidden_size

    long_term_df: pd.DataFrame = Field(
        default_factory=lambda: pd.DataFrame(columns=["user_input", "response", "embedding"])
    )
    short_term_df: pd.DataFrame = Field(
        default_factory=lambda: pd.DataFrame(columns=["user_input", "response", "embedding"])
    )

    def _generate_embedding(self, text: str) -> np.ndarray:
        """
        Core embedding generation method, meant to be overwritten by subclasses.
        This is where the actual embedding logic resides.
        """
        # Placeholder embedding generation logic (to be overwritten by subclasses)
        embedding = np.random.rand(self.embedding_size).astype(np.float32)  # Simulated embedding output
        return embedding

    def store_memory(self, user_input: str, response: str) -> None:
        """
        Store memory (short-term and long-term) along with generated embeddings.
        :param user_input: Input provided by the user.
        :param response: System's response to the input.
        """
        combined_text = user_input + " " + response

        # Generate fixed-size embedding
        embedding = self._generate_embedding(combined_text)

        # Store the memory using the SimpleMemory method
        super().store_memory(user_input, response, embedding)

    def embedding_search(self, query: str, memory_df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
        """Search for the top N closest matches based on embeddings in the provided memory DataFrame."""
        query_embedding = self._generate_embedding(query)  # Generate the embedding for the query

        # Extract the stored embeddings from the memory DataFrame
        embeddings = np.vstack(memory_df['embedding'].values)

        # Calculate cosine similarities between query embedding and stored embeddings
        similarities = cosine_similarity([query_embedding], embeddings).flatten()

        # Get the top N most similar memories based on cosine similarity
        top_indices = np.argsort(-similarities)[:top_n]

        # Return the top N matching memories
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
