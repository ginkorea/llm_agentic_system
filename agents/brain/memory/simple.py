import pandas as pd
import numpy as np
from pydantic import Field
from langchain.memory.combined import BaseMemory
from typing import Dict, List


class SimpleMemory(BaseMemory):
    """
    A memory class using Pandas DataFrame to store both short-term and long-term memory
    alongside TF-IDF-based searches or embeddings.
    """
    embedded: bool = False

    short_term_df: pd.DataFrame = Field(
        default_factory=lambda: pd.DataFrame(columns=["user_input", "response", "embedding"]))
    long_term_df: pd.DataFrame = Field(
        default_factory=lambda: pd.DataFrame(columns=["user_input", "response", "embedding"]))
    forget_threshold: int = Field(default=10)
    verbose: bool = Field(default=False)

    def store_memory(self, user_input: str, response: str, embedding: np.ndarray = None) -> None:
        """
        Store a new user input, response, and optional vectorized embedding into the short-term memory.
        Long-term memory never forgets, but short-term memory discards older entries as per the forget_threshold.

        :param user_input: User query or input.
        :param response: Model response.
        :param embedding: Optional vector embedding for search.
        """
        new_memory = pd.DataFrame([{"user_input": user_input, "response": response, "embedding": embedding}])

        # Store in short-term memory
        self.short_term_df = pd.concat([self.short_term_df, new_memory], ignore_index=True)

        # Forget the oldest memory if exceeding a threshold in short-term memory
        if len(self.short_term_df) > self.forget_threshold:
            self.short_term_df = self.short_term_df.iloc[1:]  # Remove the first (oldest) row

        # Always store in long-term memory (no forgetting)
        self.long_term_df = pd.concat([self.long_term_df, new_memory], ignore_index=True)

    def recall_memory(self, start: int, end: int, long_term: bool = False) -> pd.DataFrame:
        """
        Recall memory entries between the specified start and end indices.
        Choose whether to recall from short-term or long-term memory.

        :param start: The starting index for recall.
        :param end: The ending index for recall.
        :param long_term: Boolean flag to determine whether to recall from long-term memory.
        :return: DataFrame containing the recalled memories.
        """
        return self.long_term_df.iloc[start:end] if long_term else self.short_term_df.iloc[start:end]

    def clean_memory(self, long_term: bool = False) -> None:
        """
        Clear either short-term or long-term memory.

        :param long_term: Boolean flag to determine whether to clear long-term memory.
        """
        if long_term:
            self.long_term_df = pd.DataFrame(columns=["user_input", "response", "embedding"])
        else:
            self.short_term_df = pd.DataFrame(columns=["user_input", "response", "embedding"])

    def tfidf_search(self, query: str, long_term: bool = False, vectorizer=None) -> pd.DataFrame:
        """
        Perform a basic TF-IDF search on the stored memory (short-term or long-term).

        :param query: The search query used to find relevant memories.
        :param long_term: Boolean flag to determine if long-term memory should be searched.
        :param vectorizer: Optional vectorizer (will use default if none provided).
        :return: DataFrame of the top 5 search results based on similarity.
        """
        if vectorizer is None:
            from sklearn.feature_extraction.text import TfidfVectorizer
            vectorizer = TfidfVectorizer(stop_words="english")

        memory_df = self.long_term_df if long_term else self.short_term_df
        corpus = memory_df["user_input"] + " " + memory_df["response"]
        tfidf_matrix = vectorizer.fit_transform(corpus)
        query_vec = vectorizer.transform([query])
        cosine_similarities = np.dot(tfidf_matrix.toarray(), query_vec.toarray().T).flatten()

        top_indices = np.argsort(-cosine_similarities)[:5]
        return memory_df.iloc[top_indices]

    def save_to_csv(self, filename: str, long_term: bool = False) -> None:
        """
        Save either short-term or long-term memory DataFrame to a CSV file.

        :param filename: The file path to save the memory to.
        :param long_term: Boolean flag to determine if saving long-term memory.
        """
        memory_df = self.long_term_df if long_term else self.short_term_df
        memory_df.to_csv(filename, index=False)

    def load_from_csv(self, filename: str, long_term: bool = False) -> None:
        """
        Load either short-term or long-term memory DataFrame from a CSV file.

        :param filename: The file path to load the memory from.
        :param long_term: Boolean flag to determine if loading long-term memory.
        """
        if long_term:
            self.long_term_df = pd.read_csv(filename)
        else:
            self.short_term_df = pd.read_csv(filename)

    # Abstract methods required by BaseMemory
    def clear(self) -> None:
        """Clear all memory (both short-term and long-term)."""
        self.clean_memory(long_term=False)
        self.clean_memory(long_term=True)

    def load_memory_variables(self, inputs: Dict[str, str]) -> dict[str, dict]:
        """
        Load memory variables for the current context.
        :param inputs: Dictionary of input variables for the memory system.
        :return: A dictionary of memory variables to be used.
        """
        return {"memory_context": self.short_term_df.to_dict()}

    @property
    def memory_variables(self) -> List[str]:
        """
        Specify which memory variables are managed by this memory system.
        :return: A list of strings representing memory variable names.
        """
        return ["memory_context"]

    def save_context(self, inputs: Dict[str, str], outputs: Dict[str, str]) -> None:
        """
        Save the context of a conversation by storing user inputs and model outputs.
        :param inputs: Dictionary of input values (e.g., user queries).
        :param outputs: Dictionary of output values (e.g., model responses).
        """
        self.store_memory(inputs.get("user_input", ""), outputs.get("response", ""))


