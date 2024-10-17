from transformers import AutoTokenizer, AutoModel, AutoConfig
import torch
import numpy as np
from pydantic import Field, PrivateAttr, ConfigDict
from agents.brain.memory.embedded import EmbeddedMemory
from pandas import DataFrame

class CudaMemoryWithEmbeddings(EmbeddedMemory):
    """Memory class that uses CUDA for acceleration."""

    # Pydantic field to manage the device attribute
    device: torch.device = Field(
        default_factory=lambda: torch.device("cuda" if torch.cuda.is_available() else "cpu")
    )

    # Define Pydantic model configuration to avoid conflicts with reserved names
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
        """Generate text embeddings using CUDA."""
        inputs = self._tokenizer(
            text, return_tensors="pt", padding=True, truncation=True
        ).to(self.device)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        with torch.no_grad():
            result = self._model(
                input_ids=input_ids, attention_mask=attention_mask
            ).last_hidden_state

        # Perform mean pooling over the sequence length dimension to get a fixed-size vector
        embedding = result.mean(dim=1).cpu().numpy().flatten()

        return embedding


if __name__ == "__main__":
    # Initialize CUDA-based memory class
    memory = CudaMemoryWithEmbeddings(forget_threshold=3)

    print("\n--- Running Basic Store Memory Test ---")
    # Store some memory
    memory.store_memory("How to bake a cake?", "Mix flour, sugar, eggs, and bake.")
    memory.store_memory("How to fix a car?", "Check the engine and tires.")
    memory.store_memory("How to ride a bike?", "Start pedaling while balancing.")

    # Verify that memory was stored
    print(f"Number of entries in long-term memory: {len(memory.long_term_df)}")
    assert len(memory.long_term_df) == 3, "Memory storage failed."

    print("\n--- Running Embedding Generation Test ---")
    # Check if embeddings were generated and stored as numpy arrays
    assert isinstance(
        memory.long_term_df.iloc[0]["embedding"], np.ndarray
    ), "Embedding should be a numpy array."
    print(
        f"Shape of embedding for first entry: {memory.long_term_df.iloc[0]['embedding'].shape}"
    )

    # Ensure that embeddings have the correct size
    expected_embedding_size = memory.max_embedding_size
    print(f"Expected embedding size: {expected_embedding_size}")
    assert (
        memory.long_term_df.iloc[0]["embedding"].shape[0] == expected_embedding_size
    ), f"Embedding size should be {expected_embedding_size}, got {memory.long_term_df.iloc[0]['embedding'].shape[0]}."

    print("\n--- Running Embedding Search Test ---")
    # Perform an embedding search
    search_results = memory.search_memory("bike", top_n=1)

    # Check if search results returned data
    print(f"Search results:\n{search_results}")
    assert not search_results.empty, "Search results should not be empty."

    print("\nAll tests passed successfully.")
