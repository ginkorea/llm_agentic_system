from datetime import time

from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import numpy as np
from transformers import AutoTokenizer
from agents.brain.memory.simple import Memory
from openvino.runtime import Core

class MemoryWithEmbeddings(Memory):
    """Memory class that uses text embeddings for semantic similarity and OpenVINO for acceleration."""

    def __init__(self, forget_threshold: int = 10):
        super().__init__(forget_threshold)
        # add timing for initialization of OpenVINO and tokenizer write code now

        # Initialize OpenVINO runtime and load model
        self.ie = Core()
        self.model_path = "/home/gompert/workspace/llmas/agents/brain/memory/model_onnx/model_fp16.onnx"
        self.compiled_model = self.ie.compile_model(model=self.model_path, device_name="GPU")  # Switch to NPU if available

        # Get input/output layers for OpenVINO model
        self.input_ids = self.compiled_model.input(0)
        self.attention_mask = self.compiled_model.input(1)
        self.output_layer = self.compiled_model.output(0)

        # Initialize tokenizer (assume you have the correct tokenizer for the model)
        self.tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v3")

        # Store memory embeddings
        self.embeddings = []
        self.max_embedding_length = 32  # Define a max length to pad/truncate to

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate text embeddings using the OpenVINO-accelerated ONNX model."""
        inputs = self.tokenizer(text, return_tensors="np", padding=True, truncation=True)
        input_ids = inputs["input_ids"].astype(np.int64)
        attention_mask = inputs["attention_mask"].astype(np.int64)

        # Run inference on the OpenVINO-accelerated model
        result = self.compiled_model([input_ids, attention_mask])[self.output_layer]

        # Pad or truncate the result to a fixed length
        if result.shape[1] < self.max_embedding_length:
            # Pad with zeros
            padding = np.zeros((result.shape[0], self.max_embedding_length - result.shape[1], result.shape[2]))
            result = np.concatenate([result, padding], axis=1)
        elif result.shape[1] > self.max_embedding_length:
            # Truncate
            result = result[:, :self.max_embedding_length, :]

        # Flatten the embedding to be 2D
        result_flattened = result.reshape(-1)

        return result_flattened

    def store_memory(self, user_input: str, response: str) -> None:
        """Store memory and generate embeddings using NPU acceleration."""
        super().store_memory(user_input, response)
        combined_text = user_input + " " + response
        embedding = self._generate_embedding(combined_text)  # Generate embedding using OpenVINO
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
        """Search memory using NPU-accelerated text embeddings for semantic similarity."""
        return self.embedding_search(query)



# Test the NPU-accelerated Memory System with Sentence-Transformers
if __name__ == "__main__":
    memory = MemoryWithEmbeddings(forget_threshold=25)
    print("Memory System with NPU-accelerated Text Embeddings and OpenVINO initialized.")

    # Storing memory entries
    memory.store_memory("How do I multiply matrices?", "You can multiply matrices by following these rules...")
    memory.store_memory("What's the weather today?", "Today's weather is sunny with a high of 75 degrees.")
    memory.store_memory("Tell me about quantum physics.",
                        "Quantum physics studies the behavior of matter at atomic scales.")
    memory.store_memory("How do I divide fractions?",
                        "To divide fractions, multiply by the reciprocal of the second fraction.")
    memory.store_memory("What's the capital of France?", "The capital of France is Paris.")
    memory.store_memory("Can you explain the analogy between the brain and a computer?",
                        "The brain functions like a computer, processing information and storing memory.")
    memory.store_memory("What is photosynthesis?",
                        "Photosynthesis is the process by which plants convert light into energy.")
    memory.store_memory("What's the theory of relativity?",
                        "Einstein's theory of relativity describes how time and space are interconnected.")
    memory.store_memory("What are the laws of thermodynamics?",
                        "The laws of thermodynamics describe the principles of heat, energy, and work.")
    memory.store_memory("Can you explain gravity?", "Gravity is the force that attracts objects towards one another.")
    memory.store_memory("What is Newton's second law?",
                        "Newton's second law states that force equals mass times acceleration (F=ma).")
    memory.store_memory("How does an electric motor work?", "An electric motor converts electrical energy into motion.")
    memory.store_memory("What is the capital of Japan?", "The capital of Japan is Tokyo.")
    memory.store_memory("How do I integrate functions?", "To integrate a function, find its antiderivative.")
    memory.store_memory("What is the Pythagorean theorem?", "The Pythagorean theorem states that a^2 + b^2 = c^2.")
    memory.store_memory("How do I make a cake?", "To make a cake, you'll need flour, sugar, eggs, and baking powder.")
    memory.store_memory("What is the square root of 144?", "The square root of 144 is 12.")
    memory.store_memory("Why is Japan known as the Land of the Rising Sun?",
                        "Japan is called the Land of the Rising Sun because it lies to the east of China.")
    memory.store_memory("What is the difference between mass and weight?", "Mass is the amount of matter in an object, while weight is the force of gravity acting on it.")
    memory.store_memory("What is the speed of light?", "The speed of light in a vacuum is approximately 299,792 kilometers per second.")

    print ("Memory entries stored.")

    # Performing searches
    query_1 = "matrix multiplication"
    query_2 = "capital city of France"
    query_3 = "thermodynamics laws"
    query_4 = "gravity and force"
    query_5 = "east asian politics"
    query_6 = "island nation in the Pacific"

    # Search results using NPU-accelerated embeddings
    print(f"Search results for '{query_1}':")
    print(memory.search_memory(query_1))

    print(f"Search results for '{query_2}':")
    print(memory.search_memory(query_2))

    print(f"Search results for '{query_3}':")
    print(memory.search_memory(query_3))

    print(f"Search results for '{query_4}':")
    print(memory.search_memory(query_4))

    print(f"Search results for '{query_5}':")
    print(memory.search_memory(query_5))

    print(f"Search results for '{query_6}':")
    print(memory.search_memory(query_6))


