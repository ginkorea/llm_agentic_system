# embedded.py

import numpy as np
import pandas as pd
from agents.brain.memory.simple import SimpleMemory
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddedMemory(SimpleMemory):
    """Memory class with embedding capabilities for storage and search."""

    embedded: bool = True
    embedding_size: int = 1024  # Set to match model's hidden size


    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embeddings from input text."""
        embedding = np.zeros(self.embedding_size, dtype=np.float32)
        text_vector = np.array([ord(char) for char in text], dtype=np.float32)

        if len(text_vector) > self.embedding_size:
            embedding = text_vector[:self.embedding_size]
        else:
            embedding[:len(text_vector)] = text_vector
        return embedding

    def store_memory(self, user_input: str, response, embedding: np.ndarray = None, module: str = "") -> None:
        """
        Store memory with an embedding generated from input and response.
        """
        # Ensure response is converted to a string if necessary
        response_str = response if isinstance(response, str) else str(response)

        # Generate embedding from combined text
        combined_text = user_input + " " + response_str
        embedding = embedding or self._generate_embedding(combined_text)

        # Call the superclass store_memory to actually store the memory entry
        super().store_memory(user_input, response_str, embedding, module)

    def embedding_search(self, query: str, memory_df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
        """Search for the top N closest matches using embeddings."""
        query_embedding = self._generate_embedding(query)

        # Compute cosine similarities with stored embeddings
        embeddings = np.vstack(memory_df['embedding'].values)
        similarities = cosine_similarity([query_embedding], embeddings).flatten()
        top_indices = np.argsort(-similarities)[:top_n]

        return memory_df.iloc[top_indices]

    def search_memory(self, query: str, long_term: bool = True, top_n: int = 3) -> pd.DataFrame:
        """Perform an embedding search, with an option to search long-term memory."""
        memory_df = self.long_term_df if long_term else self.long_term_df.head(self.short_term_length)
        return self.embedding_search(query, memory_df, top_n)



# Test the class
if __name__ == "__main__":
    memory = EmbeddedMemory()
    sample_text = "Test embedding generation"
    test_embedding = memory._generate_embedding(sample_text)
    print(f"Generated embedding: {test_embedding}")
