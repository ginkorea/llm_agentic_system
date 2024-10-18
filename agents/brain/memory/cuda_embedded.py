from transformers import AutoTokenizer, AutoModel, AutoConfig
import torch
import numpy as np
from pydantic import Field, PrivateAttr, ConfigDict
from agents.brain.memory.embedded import EmbeddedMemory
from agents.brain.memory.model.get import Models

class CudaMemoryWithEmbeddings(EmbeddedMemory):
    """Memory class that uses CUDA for acceleration with dynamic model and tokenizer management."""

    # Pydantic model configuration to avoid conflicts
    model_config = ConfigDict(protected_namespaces=())

    # Pydantic-managed fields
    model_name: str = Field(default="")
    model_path: str = Field(default="")
    device: torch.device = Field(
        default_factory=lambda: torch.device("cuda" if torch.cuda.is_available() else "cpu")
    )

    # Private attributes for the model and tokenizer
    _model: AutoModel = PrivateAttr()
    _tokenizer: AutoTokenizer = PrivateAttr()

    def __init__(self, **kwargs):
        """Initialize CUDA-based memory and set up the model and tokenizer."""
        # Extract keyword arguments for model directory index and model name if provided
        model_dir_index = kwargs.pop('model_dir_index', 0)  # Default to index 0
        model_name = kwargs.pop('model_name', "")  # Use default model_name if not provided

        super().__init__(**kwargs)  # Initialize Pydantic fields using kwargs

        # Get model paths and tokenizer using the Models class
        models = Models()
        model_dir = models.get_model_dir()[model_dir_index]  # Allow directory index to be specified dynamically
        print(f"Selected model directory: {model_dir}")
        self.model_path = f"{model_dir}/{model_name}"
        tokenizer_name = models.tokenizers[model_dir_index]  # Choose tokenizer based on the same index

        # Load model configuration
        config = AutoConfig.from_pretrained(model_dir, trust_remote_code=True)

        # Update embedding size based on model's hidden size
        self.embedding_size = config.hidden_size

        # Load tokenizer
        self._tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, trust_remote_code=True)

        # Load the model and move it to the appropriate device (CUDA or CPU)
        self._model = AutoModel.from_pretrained(model_dir, config=config, trust_remote_code=True).to(self.device)

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate text embeddings using mean pooling."""
        inputs = self._tokenizer(
            text, return_tensors="pt", padding=True, truncation=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self._model(**inputs)
            last_hidden_state = outputs.last_hidden_state

        # Mean pooling to get fixed-size vector
        embedding = last_hidden_state.mean(dim=1).cpu().numpy().flatten()

        return embedding

if __name__ == "__main__":
    # Initialize CUDA-based memory class with dynamic directory index and model name
    memory = CudaMemoryWithEmbeddings(forget_threshold=3, model_dir_index=2)

    # Test the memory class
    from agents.brain.memory.test import memory_tests
    memory_tests(memory)
