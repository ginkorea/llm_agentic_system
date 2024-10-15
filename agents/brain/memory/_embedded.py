from datetime import time
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import numpy as np
from transformers import AutoTokenizer, AutoModel
from agents.brain.memory.simple import Memory
from openvino.runtime import Core
import torch
import os

class MemoryWithEmbeddings(Memory):
    def __init__(self, forget_threshold: int = 10, max_embedding_length: int = 32):
        super().__init__(forget_threshold)
        self.cuda = torch.cuda.is_available()
        self.using = None

        model_dir = "model/jina-embeddings-v3"
        print(f"The path {model_dir} exists: {os.path.exists(model_dir)}")

        if not os.path.exists(model_dir):
            raise ValueError(f"Model directory does not exist: {model_dir}")

        # Check if CUDA is available and use CUDA if possible
        if self.cuda and os.path.exists(model_dir + '/pytorch_model.bin'):
            print("CUDA is available. Using CUDA for acceleration.")
            self.using = "cuda"
            self.device = torch.device(self.using)
            self.model = AutoModel.from_pretrained(model_dir, trust_remote_code=True).to(self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

        elif os.path.exists(model_dir + '/model_fp16.onnx'):
            print("CUDA not available or not chosen. Falling back to OpenVINO.")
            self.using = "openvino"
            self.ie = Core()
            self.model_path = model_dir + "/model_fp16.onnx"
            self.compiled_model = self.ie.compile_model(model=self.model_path, device_name="CPU")
            self.input_ids = self.compiled_model.input(0)
            self.attention_mask = self.compiled_model.input(1)
            self.output_layer = self.compiled_model.output(0)
            # Initialize tokenizer here only if necessary for ONNX
            self.tokenizer = AutoTokenizer.from_pretrained(model_dir)  # Adjust this if ONNX needs the tokenizer
        else:
            raise ValueError("No suitable model found (CUDA or ONNX).")


    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate text embeddings using either CUDA or OpenVINO, depending on availability."""
        # Tokenize the input text
        inputs = self.tokenizer(text, return_tensors="pt" if torch.cuda.is_available() else "np", padding=True,
                                truncation=True)

        if torch.cuda.is_available():
            # Ensure input_ids are cast to LongTensor (int64) as required by the embedding layer
            input_ids = inputs["input_ids"].to(self.device).long()  # Cast to LongTensor
            attention_mask = inputs["attention_mask"].to(self.device).float()  # Cast to Float32

            with torch.no_grad():
                # Cast model output to Float32 to avoid BFloat16 precision errors
                result = self.model(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state.to(
                    torch.float32).cpu().numpy()
        else:
            # OpenVINO inference
            input_ids = inputs["input_ids"].astype(np.int64)  # Ensure correct int type for OpenVINO
            attention_mask = inputs["attention_mask"].astype(np.float32)  # Ensure Float32 for OpenVINO
            result = self.compiled_model([input_ids, attention_mask])[self.output_layer]

        # Pad or truncate the result to a fixed length
        if result.shape[1] < self.max_embedding_length:
            padding = np.zeros((result.shape[0], self.max_embedding_length - result.shape[1], result.shape[2]),
                               dtype=np.float32)
            result = np.concatenate([result, padding], axis=1)
        elif result.shape[1] > self.max_embedding_length:
            result = result[:, :self.max_embedding_length, :]

        # Return the flattened embedding
        return result.reshape(-1)

    def store_memory(self, user_input: str, response: str) -> None:
        """Store memory and generate embeddings using either CUDA or OpenVINO."""
        super().store_memory(user_input, response)
        combined_text = user_input + " " + response
        embedding = self._generate_embedding(combined_text)  # Generate embedding using either CUDA or OpenVINO
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
        """Search memory using CUDA or OpenVINO-accelerated text embeddings for semantic similarity."""
        return self.embedding_search(query)


# Test the Memory System with CUDA/OpenVINO acceleration
if __name__ == "__main__":
    memory = MemoryWithEmbeddings(forget_threshold=25)
    print(f"Memory System initialized with dynamic CUDA/OpenVINO selection. Using {memory.using}")

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

    print("Memory entries stored.")

    # Performing searches
    query_1 = "matrix multiplication"
    query_2 = "capital city of France"
    query_3 = "thermodynamics laws"
    query_4 = "gravity and force"
    query_5 = "east asian politics"
    query_6 = "island nation in the Pacific"

    # Search results using CUDA/OpenVINO-accelerated embeddings
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
