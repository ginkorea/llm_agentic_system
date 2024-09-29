from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict
import numpy as np


class Memory:
    def __init__(self, forget_threshold: int = 10):
        self.long_term = []
        self.short_term = []
        self.forget_threshold = forget_threshold

    def store_memory(self, user_input: str, response: str) -> None:
        self.short_term.append({"user_input": user_input, "response": response})
        if len(self.short_term) > self.forget_threshold:
            self.short_term.pop(0)
        self.long_term.append({"user_input": user_input, "response": response})

    def recall_memory(self, start: int, end: int, long_term: bool = False) -> List[Dict[str, str]]:
        return self.long_term[start:end] if long_term else self.short_term[start:end]

    def clean_memory(self, long_term: bool = False) -> None:
        self.long_term = [] if long_term else []

    def tfidf_search(self, query: str, long_term: bool = False) -> List[Dict[str, str]]:
        """Perform a basic TF-IDF search on the memory."""
        memory_data = self.long_term if long_term else self.short_term
        corpus = [item["user_input"] + " " + item["response"] for item in memory_data]

        if not corpus:
            return []

        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Transform the query and find the cosine similarity
        query_vec = vectorizer.transform([query])
        cosine_similarities = np.dot(tfidf_matrix, query_vec.T).toarray().flatten()

        # Rank by cosine similarity
        ranked_indices = np.argsort(-cosine_similarities)

        return [memory_data[idx] for idx in ranked_indices[:5]]  # Return top 5 matches

    def search_memory(self, query: str, long_term: bool = False) -> List[Dict[str, str]]:
        return self.tfidf_search(query, long_term)

if __name__ == "__main__":
    memory = Memory(forget_threshold=25)

    # Storing diverse memory entries
    memory.store_memory("How do I multiply matrices?", "You can multiply matrices by following these rules...")
    memory.store_memory("What's the weather today?", "Today's weather is sunny with a high of 75.")
    memory.store_memory("Tell me about quantum physics.",
                        "Quantum physics explores the behavior of matter at atomic scales.")
    memory.store_memory("How do I divide fractions?",
                        "To divide fractions, multiply by the reciprocal of the second fraction.")
    memory.store_memory("What's the capital of France?", "The capital of France is Paris.")
    memory.store_memory("How can I find the determinant of a matrix?",
                        "You can calculate the determinant using cofactor expansion.")
    memory.store_memory("How do I make a cake?", "To make a cake, you'll need flour, sugar, eggs, and baking powder.")
    memory.store_memory("Can you explain the analogy of the universe to a computer?",
                        "The universe works like a giant computer processing information.")
    memory.store_memory("How does an electric motor work?",
                        "An electric motor converts electrical energy into mechanical energy using electromagnetism.")
    memory.store_memory("What's the square root of 144?", "The square root of 144 is 12.")
    memory.store_memory("How does gravity work?", "Gravity is a force of attraction between two masses.")
    memory.store_memory("What is the theory of relativity?",
                        "Einstein's theory of relativity describes the relationship between space and time.")
    memory.store_memory("How do I integrate functions?", "To integrate a function, find its antiderivative.")
    memory.store_memory("What's the difference between AI and machine learning?",
                        "AI is the broader field, while machine learning is a subset focusing on training algorithms.")
    memory.store_memory("How do I multiply numbers in my head?",
                        "You can break down the numbers into simpler components, multiplying them part by part.")
    memory.store_memory("Can you explain entropy in thermodynamics?",
                        "Entropy is a measure of disorder in a thermodynamic system.")
    memory.store_memory("What's the analogy between neurons and electronic circuits?",
                        "Neurons in the brain function similarly to transistors in an electronic circuit.")
    memory.store_memory("How do plants photosynthesize?",
                        "Photosynthesis is the process by which plants convert light into chemical energy.")
    memory.store_memory("What is the Pythagorean theorem?",
                        "The Pythagorean theorem states that in a right triangle, a² + b² = c².")
    memory.store_memory("What's a metaphor for time?", "Time is often compared to a river, constantly flowing forward.")
    memory.store_memory("What are prime numbers?",
                        "Prime numbers are numbers greater than 1 that are divisible only by 1 and themselves.")
    memory.store_memory("Explain Newton's laws of motion.",
                        "Newton's laws describe how objects move under the influence of forces.")
    memory.store_memory("How do I solve quadratic equations?",
                        "You can solve quadratic equations using the quadratic formula.")
    memory.store_memory("How do computers store memory?",
                        "Computers store memory using bits and bytes in RAM and hard drives.")
    memory.store_memory("What's the analogy of the human brain to a network?",
                        "The human brain is like a vast neural network, with neurons as interconnected nodes.")
    memory.store_memory("How do I convert Celsius to Fahrenheit?", "To convert Celsius to Fahrenheit, use the formula...")
    memory.store_memory("raw dogging it", "raw dogging it is a term used")
    memory.store_memory("is sex with a hooker considered raw dogging it", "yes")
    memory.store_memory("sex workers in Puerto Rico", "hookers in Puerto Rico are called putas")

    # Performing a search in memory
    search_results = memory.search_memory("chaos and order")
    print("Search results for 'chaos and order':")
    print(search_results)

    search_results = memory.search_memory("analogy")
    print("Search results for 'analogy':")
    print(search_results)

    search_results = memory.search_memory("Pythagorean")
    print("Search results for 'Pythagorean':")
    print(search_results)

    search_results = memory.search_memory("sex")
    print("Search results for 'sex':")
    print(search_results)
