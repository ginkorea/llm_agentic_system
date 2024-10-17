import numpy as np
from pandas import DataFrame
from transformers import AutoTokenizer
from openvino.runtime import Core
from pydantic import Field, PrivateAttr, ConfigDict
from agents.brain.memory.embedded import EmbeddedMemory

class OpenvinoMemoryWithEmbeddings(EmbeddedMemory):
    """Memory class that uses OpenVINO for acceleration."""

    model_path: str = Field(default="model/jina-embeddings-v3/model_fp16.onnx")
    ie: Core = Field(default_factory=Core)

    # Define Pydantic model configuration to avoid conflict with "model_"
    model_config = ConfigDict(protected_namespaces=())

    # Use private attributes for dynamic objects
    _compiled_model: Core = PrivateAttr()
    _tokenizer: AutoTokenizer = PrivateAttr()

    def __init__(self, **kwargs):
        """Initialize OpenVINO memory and compile model."""
        super().__init__(**kwargs)

        # Compile the OpenVINO model
        device_to_use = "GPU" if self.ie.get_versions("GPU") else "CPU"
        self._compiled_model = self.ie.compile_model(model=self.model_path, device_name=device_to_use)

        # Initialize tokenizer
        self._tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v3")

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate text embeddings using the OpenVINO-accelerated ONNX model."""
        inputs = self._tokenizer(text, return_tensors="np", padding=True)
        input_ids = inputs["input_ids"].astype(np.int64)
        attention_mask = inputs["attention_mask"].astype(np.int64)

        # Run inference on OpenVINO model
        result = self._compiled_model([input_ids, attention_mask])

        return result[self._compiled_model.output(0)].flatten()


if __name__ == "__main__":
    # Initialize OpenVINO-based memory class
    memory = OpenvinoMemoryWithEmbeddings(forget_threshold=3)

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
    assert isinstance(memory.long_term_df.iloc[0]["embedding"], np.ndarray), "Embedding should be a numpy array."
    print(f"Shape of embedding for first entry: {memory.long_term_df.iloc[0]['embedding'].shape}")

    # Ensure that embeddings have the correct size (this assumes the max embedding size)
    expected_embedding_size = memory.max_embedding_size  # Adjust this based on your model
    print(f"Expected embedding size: {expected_embedding_size}")
    assert memory.long_term_df.iloc[0]["embedding"].shape[0] == expected_embedding_size, \
        f"Embedding size should be {expected_embedding_size}, got {memory.long_term_df.iloc[0]['embedding'].shape[0]}."

    print("\n--- Running Embedding Search Test ---")
    # Perform an embedding search
    search_results = memory.search_memory("bike", top_n=1)

    # Check if search results returned data
    print(f"Search results:\n{search_results}")
    assert not search_results.empty, "Search results should not be empty."

    print("\nAll tests passed successfully.")
