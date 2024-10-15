from typing import Dict, List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from agents.brain.memory.simple import Memory

class EmbeddedMemory(Memory):
    """Base memory class that provides shared functionality for embedding storage and search."""

    def __init__(self, forget_threshold: int = 10, max_embedding_length: int = 32):
        super().__init__(forget_threshold)
        self.embeddings = []
        self.max_embedding_length = max_embedding_length

    def _pad_or_truncate(self, result: np.ndarray) -> np.ndarray:
        """Pad or truncate the result to a fixed length."""
        if result.shape[1] < self.max_embedding_length:
            # Pad with zeros
            padding = np.zeros((result.shape[0], self.max_embedding_length - result.shape[1], result.shape[2]))
            result = np.concatenate([result, padding], axis=1)
        elif result.shape[1] > self.max_embedding_length:
            # Truncate to max length
            result = result[:, :self.max_embedding_length, :]

        return result

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Placeholder method for generating embeddings (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement _generate_embedding")

    def store_memory(self, user_input: str, response: str) -> None:
        """Store memory and generate embeddings using specific acceleration (CUDA/OpenVINO)."""
        super().store_memory(user_input, response)
        combined_text = user_input + " " + response
        embedding = self._generate_embedding(combined_text)  # Call the subclass's embedding generator
        self.embeddings.append(embedding)

    def embedding_search(self, query: str, top_n: int = 3) -> List[Dict[str, str]]:
        """Search memory using text embeddings for semantic similarity."""
        if not self.embeddings:
            return []

        query_embedding = self._generate_embedding(query)

        # Compute cosine similarity
        similarities = cosine_similarity([query_embedding], self.embeddings).flatten()
        ranked_indices = np.argsort(-similarities)

        return [self.long_term[idx] for idx in ranked_indices[:top_n]]

    def search_memory(self, query: str, long_term: bool = False) -> List[Dict[str, str]]:
        """Search memory using accelerated text embeddings for semantic similarity."""
        return self.embedding_search(query)
