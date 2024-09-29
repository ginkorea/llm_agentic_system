from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import numpy as np
from agents.brain.memory.simple import Memory

class MemoryWithEmbeddings(Memory):
    """Memory class that uses text embeddings for semantic similarity."""
    def __init__(self, forget_threshold: int = 10):
        super().__init__(forget_threshold)
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Small and efficient embedding model
        self.embeddings = []

    def store_memory(self, user_input: str, response: str) -> None:
        super().store_memory(user_input, response)
        combined_text = user_input + " " + response
        embedding = self.model.encode(combined_text)
        self.embeddings.append(embedding)

    def embedding_search(self, query: str, top_n: int = 3) -> List[Dict[str, str]]:
        """Search memory using text embeddings for semantic similarity."""
        if not self.embeddings:
            return []

        query_embedding = self.model.encode(query)
        similarities = cosine_similarity([query_embedding], self.embeddings).flatten()
        ranked_indices = np.argsort(-similarities)

        return [self.long_term[idx] for idx in ranked_indices[:top_n]]

    def search_memory(self, query: str, long_term: bool = False) -> List[Dict[str, str]]:
        """Search memory using text embeddings for semantic similarity."""
        return self.embedding_search(query)



