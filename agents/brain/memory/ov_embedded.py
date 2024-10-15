from transformers import AutoTokenizer
from openvino.runtime import Core
import numpy as np
from agents.brain.memory.embedded import EmbeddedMemory

class OpenvinoMemoryWithEmbeddings(EmbeddedMemory):
    """Memory class that uses OpenVINO for acceleration."""

    def __init__(self, forget_threshold: int = 10):
        super().__init__(forget_threshold)

        # Initialize OpenVINO runtime and load model
        self.ie = Core()
        self.model_path = "model/jina-embeddings-v3/model_fp16.onnx"
        self.compiled_model = self.ie.compile_model(model=self.model_path, device_name="GPU")

        # Get input/output layers for OpenVINO model
        self.input_ids = self.compiled_model.input(0)
        self.attention_mask = self.compiled_model.input(1)
        self.output_layer = self.compiled_model.output(0)

        # Initialize tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v3")

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate text embeddings using the OpenVINO-accelerated ONNX model."""
        inputs = self.tokenizer(text, return_tensors="np", padding=True, truncation=True)
        input_ids = inputs["input_ids"].astype(np.int64)
        attention_mask = inputs["attention_mask"].astype(np.int64)

        # Run inference on OpenVINO model
        result = self.compiled_model([input_ids, attention_mask])[self.output_layer]

        # Use the shared padding/truncation method from the base class
        return self._pad_or_truncate(result).flatten()
