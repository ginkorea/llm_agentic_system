import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import Field
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
        """Generate embeddings from input text without any acceleration."""

        # Here, we create a basic embedding by averaging character ASCII values
        embedding = np.zeros(self.embedding_size, dtype=np.float32)

        # Create a simple text vectorization (e.g., bag-of-words or character embedding)
        text_vector = np.array([ord(char) for char in text], dtype=np.float32)

        # Pad or truncate to match the embedding size
        if len(text_vector) > self.embedding_size:
            embedding = text_vector[:self.embedding_size]  # Truncate
        else:
            embedding[:len(text_vector)] = text_vector  # Fill with text vector

        return embedding

    def store_memory(self, user_input: str, response: str) -> None:
        """Store memory (short-term and long-term) along with generated embeddings."""
        combined_text = user_input + " " + response

        # Generate fixed-size embedding
        embedding = self._generate_embedding(combined_text)

        # Store the memory using the SimpleMemory method
        super().store_memory(user_input, response, embedding)

    def embedding_search(self, query: str, memory_df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
        """Search for the top N closest matches based on embeddings in the provided memory DataFrame."""
        query_embedding = self._generate_embedding(query)

        # Extract the stored embeddings from the memory DataFrame
        embeddings = np.vstack(memory_df['embedding'].values)

        # Calculate cosine similarities between query embedding and stored embeddings
        similarities = cosine_similarity([query_embedding], embeddings).flatten()

        # Get the top N most similar memories based on cosine similarity
        top_indices = np.argsort(-similarities)[:top_n]

        # Return the top N matching memories
        return memory_df.iloc[top_indices]

    def search_memory(self, query: str, long_term: bool = False, top_n: int = 3) -> pd.DataFrame:
        """Perform an embedding search on the stored memory (short-term or long-term)."""
        memory_df = self.long_term_df if long_term else self.short_term_df
        return self.embedding_search(query, memory_df, top_n)


# Test the class
if __name__ == "__main__":
    memory = EmbeddedMemory()
    sample_text = "Test embedding generation"
    embedding = memory._generate_embedding(sample_text)
    print(f"Generated embedding: {embedding}")
