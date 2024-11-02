# simple.py

import pandas as pd
import numpy as np
from pydantic import Field
from langchain.memory.combined import BaseMemory
from typing import Dict, List

class SimpleMemory(BaseMemory):
    """
    A memory class using a single Pandas DataFrame to store memory entries.
    Short-term memory is managed by dynamically setting a length limit on the head of this DataFrame.
    """
    verbose: bool = False
    embedded: bool = False
    long_term_df: pd.DataFrame = Field(
        default_factory=lambda: pd.DataFrame(columns=["user_input", "response", "embedding", "module"])
    )
    short_term_length: int = Field(default=10)  # Default, dynamically adjustable

    def set_short_term_length(self, length: int):
        """Set the short-term memory limit dynamically based on the active lobe's memory limit."""
        self.short_term_length = length

    # simple.py

    def store_memory(self, user_input: str, response, embedding: np.ndarray = None, module: str = "") -> None:
        """
        Store a new user input, response, optional vectorized embedding, and module name into memory.

        :param user_input: User query or input.
        :param response: Model response, which will be converted to a string if not already.
        :param embedding: Optional vector embedding for search.
        :param module: Name of the module or tool used for processing.
        """
        # Convert response to a string if it is not already a string
        response_str = response if isinstance(response, str) else str(response)

        new_memory = pd.DataFrame([{
            "user_input": user_input,
            "response": response_str,
            "embedding": embedding,
            "module": module
        }])
        self.long_term_df = pd.concat([self.long_term_df, new_memory], ignore_index=True)
        self.save_to_csv("memory.csv", long_term=True)
        print("Memory saved to memory.csv")

    def recall_memory(self, start: int, end: int, long_term: bool = False) -> pd.DataFrame:
        """
        Recall memory entries between the specified start and end indices.
        Use the head of long-term memory for short-term retrieval.

        :param start: The starting index for recall.
        :param end: The ending index for recall.
        :param long_term: Boolean flag to determine whether to recall from long-term memory.
        :return: DataFrame containing the recalled memories.
        """
        if long_term:
            return self.long_term_df.iloc[start:end]
        else:
            return self.long_term_df.head(self.short_term_length).iloc[start:end]

    def format_memory(self) -> List[Dict[str, str]]:
        """
        Format memory into a JSON-like structure compatible with OpenAI Chat Completion format.
        This method will return memory entries with "role" and "content" fields, reflecting past conversations.

        :return: A list of formatted memory entries as dictionaries.
        """
        recent_memory = self.long_term_df.head(self.short_term_length).to_dict('records')

        formatted_memory = []
        for entry in recent_memory:
            formatted_memory.append({"role": "user", "content": entry["user_input"]})
            formatted_memory.append({"role": "assistant", "content": entry["response"]})

        return formatted_memory


    def clean_memory(self, long_term: bool = False) -> None:
        """
        Clear either the entire long-term memory or reset the short-term length.

        :param long_term: Boolean flag to determine whether to clear long-term memory.
        """
        if long_term:
            self.long_term_df = pd.DataFrame(columns=["user_input", "response", "embedding"])

    def tfidf_search(self, query: str, long_term: bool = False, vectorizer=None) -> pd.DataFrame:
        """
        Perform a TF-IDF search on the stored memory.

        :param query: The search query used to find relevant memories.
        :param long_term: Boolean flag to determine if long-term memory should be searched.
        :param vectorizer: Optional vectorizer (will use default if none provided).
        :return: DataFrame of the top 5 search results based on similarity.
        """
        if vectorizer is None:
            from sklearn.feature_extraction.text import TfidfVectorizer
            vectorizer = TfidfVectorizer(stop_words="english")

        memory_df = self.long_term_df if long_term else self.long_term_df.head(self.short_term_length)
        corpus = memory_df["user_input"] + " " + memory_df["response"]
        tfidf_matrix = vectorizer.fit_transform(corpus)
        query_vec = vectorizer.transform([query])
        cosine_similarities = np.dot(tfidf_matrix.toarray(), query_vec.toarray().T).flatten()

        top_indices = np.argsort(-cosine_similarities)[:5]
        return memory_df.iloc[top_indices]

    def save_to_csv(self, filename: str, long_term: bool = True) -> None:
        """
        Save the memory DataFrame to a CSV file.

        :param filename: The file path to save the memory to.
        :param long_term: Boolean flag to determine if saving the full long-term memory.
        """
        memory_df = self.long_term_df if long_term else self.long_term_df.head(self.short_term_length)
        memory_df.to_csv(filename, index=False)

    def load_from_csv(self, filename: str, long_term: bool = False) -> None:
        """
        Load memory from a CSV file.

        :param filename: The file path to load the memory from.
        :param long_term: Boolean flag to determine if loading into long-term memory.
        """
        if long_term:
            self.long_term_df = pd.read_csv(filename)

    # Abstract methods required by BaseMemory
    def clear(self) -> None:
        """Clear all memory."""
        self.clean_memory(long_term=True)

    def load_memory_variables(self, inputs: Dict[str, str]) -> dict:
        """
        Load memory variables for the current context.
        :param inputs: Dictionary of input variables for the memory system.
        :return: A dictionary of memory variables to be used.
        """
        return {"memory_context": self.long_term_df.head(self.short_term_length).to_dict()}

    @property
    def memory_variables(self) -> List[str]:
        """Specify which memory variables are managed by this memory system."""
        return ["memory_context"]

    def save_context(self, inputs: Dict[str, str], outputs: Dict[str, str]) -> None:
        """
        Save the context of a conversation by storing user inputs and model outputs.
        :param inputs: Dictionary of input values (e.g., user queries).
        :param outputs: Dictionary of output values (e.g., model responses).
        """
        self.store_memory(inputs.get("user_input", ""), outputs.get("response", ""))
