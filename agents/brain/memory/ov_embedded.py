import numpy as np
from transformers import AutoTokenizer
from openvino.runtime import Core
from pydantic import Field, PrivateAttr, ConfigDict
from agents.brain.memory.embedded import EmbeddedMemory
from agents.brain.memory.model.get import Models



class OpenvinoMemoryWithEmbeddings(EmbeddedMemory):
    """Memory class that uses OpenVINO for acceleration with dynamic model selection using Pydantic."""

    model_config = ConfigDict(protected_namespaces=())
    model_name: str = Field(default="model_fp16.onnx")
    model_path: str = Field(default="")
    ie: Core = Field(default_factory=Core)

    _compiled_model: Core = PrivateAttr()
    _tokenizer: AutoTokenizer = PrivateAttr()


    def __init__(self, **kwargs):
        """Initialize OpenVINO memory and set up the selected model and tokenizer."""
        super().__init__(**kwargs)

        # Set model paths and tokenizer via Models class
        models = Models()
        model_dir = models.model_directories[0]
        self.model_path = f"{model_dir}/{self.model_name}"

        # Select tokenizer dynamically (modify based on your needs)
        tokenizer_name = models.tokenizers[0]  # You can adapt this to switch between different models

        # Compile the OpenVINO model
        device_to_use = "GPU" if "GPU" in self.ie.available_devices else "CPU"
        self._compiled_model = self.ie.compile_model(model=self.model_path, device_name=device_to_use)

        # Initialize tokenizer
        self._tokenizer = AutoTokenizer.from_pretrained(model_dir)

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate text embeddings using the OpenVINO-accelerated ONNX model."""
        max_length = 8194

        # Set a maximum sequence length
        inputs = self._tokenizer(text, return_tensors="np", padding=True, truncation=True, max_length=max_length)
        input_ids = inputs["input_ids"].astype(np.int64)
        attention_mask = inputs["attention_mask"].astype(np.int64)

        # Run inference on OpenVINO model
        result = self._compiled_model([input_ids, attention_mask])

        # Get embedding output and resize to a fixed size
        embedding = result[self._compiled_model.output(0)].flatten()
        fixed_size = self.embedding_size  # Adjust this based on your model's expected output size
        if len(embedding) > fixed_size:
            embedding = embedding[:fixed_size]
        elif len(embedding) < fixed_size:
            embedding = np.pad(embedding, (0, fixed_size - len(embedding)))

        return embedding


if __name__ == "__main__":
    # Initialize OpenVINO-based memory class
    from agents.brain.memory.test import memory_tests

    memory = OpenvinoMemoryWithEmbeddings(forget_threshold=3)

    # Run memory tests
    memory_tests(memory)
