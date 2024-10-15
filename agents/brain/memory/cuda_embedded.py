from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from agents.brain.memory.embedded import EmbeddedMemory

class CudaMemoryWithEmbeddings(EmbeddedMemory):
    """Memory class that uses CUDA for acceleration."""

    def __init__(self, forget_threshold: int = 10):
        super().__init__(forget_threshold)

        # Initialize CUDA device and model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_dir = "model/jina-embeddings-v3"

        # Load CUDA model
        self.model = AutoModel.from_pretrained(model_dir, trust_remote_code=True).to(self.device)

        # Initialize tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate text embeddings using CUDA."""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(self.device)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        with torch.no_grad():
            result = self.model(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state.cpu().numpy()

        # Use the shared padding/truncation method from the base class
        return self._pad_or_truncate(result).flatten()
