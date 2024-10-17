from transformers import AutoTokenizer, AutoModel, AutoConfig
import torch
import numpy as np
from pydantic import Field, PrivateAttr, ConfigDict
from agents.brain.memory.embedded import EmbeddedMemory

class CudaMemoryWithEmbeddings(EmbeddedMemory):
    """Memory class that uses CUDA for acceleration."""

    # Pydantic field to manage the device attribute
    device: torch.device = Field(
        default_factory=lambda: torch.device("cuda" if torch.cuda.is_available() else "cpu")
    )

    # Define Pydantic model configuration to avoid conflicts
    model_config = ConfigDict(protected_namespaces=())

    # Use private attributes for dynamic objects
    _model: AutoModel = PrivateAttr()
    _tokenizer: AutoTokenizer = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize CUDA model and tokenizer
        model_dir = "jinaai/jina-embeddings-v3"  # Use the full model name

        # Load configuration
        config = AutoConfig.from_pretrained(model_dir, trust_remote_code=True)

        # Update embedding_size based on model's hidden_size
        self.embedding_size = config.hidden_size  # For example, 1024

        # Load tokenizer
        self._tokenizer = AutoTokenizer.from_pretrained(
            model_dir, trust_remote_code=True
        )

        # Load model with configuration
        self._model = AutoModel.from_pretrained(
            model_dir,
            config=config,
            trust_remote_code=True,
        ).to(self.device)

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate text embeddings using mean pooling."""
        inputs = self._tokenizer(
            text, return_tensors="pt", padding=True, truncation=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self._model(**inputs)
            last_hidden_state = outputs.last_hidden_state  # Shape: (batch_size, sequence_length, hidden_size)

        # Mean pooling over the sequence length dimension to get a fixed-size vector
        embedding = last_hidden_state.mean(dim=1).cpu().numpy().flatten()

        return embedding  # Embedding size is hidden_size (e.g., 1024)


if __name__ == "__main__":
    # Initialize CUDA-based memory class
    memory = CudaMemoryWithEmbeddings(forget_threshold=3)

    # Test the memory class
    from agents.brain.memory.test import memory_tests

    memory_tests(memory)
