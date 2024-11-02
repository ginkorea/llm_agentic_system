from flash_attn import flash_attn_func
from transformers import AutoTokenizer, AutoModel, AutoConfig
import torch
import torch.nn.functional as F
import numpy as np
from pydantic import Field, PrivateAttr, ConfigDict
from agents.brain.memory.embedded import EmbeddedMemory
from agents.brain.memory.model.get import Models


class CudaMemoryWithEmbeddings(EmbeddedMemory):
    """Memory class that uses CUDA for acceleration with dynamic model and tokenizer management."""

    model_config = ConfigDict(protected_namespaces=())
    model_name: str = Field(default="")
    model_path: str = Field(default="")
    device: torch.device = Field(default_factory=lambda: torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    _model: AutoModel = PrivateAttr()
    _tokenizer: AutoTokenizer = PrivateAttr()

    def __init__(self, **kwargs):
        """Initialize CUDA-based memory and set up the model and tokenizer."""
        model_dir_index = kwargs.pop('model_dir_index', 2)
        model_name = kwargs.pop('model_name', "")

        super().__init__(**kwargs)

        models = Models()
        model_dir = models.get_model_dir()[model_dir_index]
        print(f"Selected model directory: {model_dir}")
        self.model_path = f"{model_dir}/{model_name}"
        tokenizer_name = models.tokenizers[model_dir_index]

        config = AutoConfig.from_pretrained(model_dir, trust_remote_code=True)

        self.embedding_size = config.hidden_size

        self._tokenizer = AutoTokenizer.from_pretrained(
            model_dir, trust_remote_code=True, clean_up_tokenization_spaces=False
        )

        self._model = AutoModel.from_pretrained(model_dir, config=config, trust_remote_code=True).to(self.device)

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Custom embedding generation using CUDA and FlashAttention."""
        inputs = self._tokenizer(
            text, return_tensors="pt", padding=True, truncation=True
        ).to(self.device)

        with torch.no_grad():
            # Forward pass through the model
            outputs = self._model(**inputs)
            hidden_state = outputs.last_hidden_state.to(self.device).to(torch.float16)
            if self.verbose:
                print(f"Shape of model output (last_hidden_state): {hidden_state.shape}")
                print(f"Dtype of model output (last_hidden_state): {hidden_state.dtype}")

            # Number of heads and head dimension
            n_heads = 12  # Adjust based on your model
            hidden_dim = hidden_state.size(-1)  # Dynamically get hidden_dim from hidden_state
            if hidden_dim % n_heads != 0:
                # Adjust hidden_dim to be divisible by n_heads
                padding_size = n_heads - (hidden_dim % n_heads)
                hidden_state = F.pad(hidden_state, (0, padding_size))
                hidden_dim = hidden_state.size(-1)

            head_dim = hidden_dim // n_heads  # Ensure head_dim * n_heads == hidden_dim
            if self.verbose:
                print(f"n_heads: {n_heads}, head_dim: {head_dim}")

            # Dynamic Linear projections for Q, K, V
            # Ensure weights are in torch.float16 and adjust to hidden_state's size
            weight_qkv = torch.randn(hidden_dim, hidden_dim, device=self.device, dtype=torch.float16)

            query = F.linear(hidden_state, weight=weight_qkv)
            key = F.linear(hidden_state, weight=weight_qkv)
            value = F.linear(hidden_state, weight=weight_qkv)

            # Reshape Q, K, V to (batch_size, seqlen, n_heads, head_dim)
            query = query.view(hidden_state.size(0), hidden_state.size(1), n_heads, head_dim)
            key = key.view(hidden_state.size(0), hidden_state.size(1), n_heads, head_dim)
            value = value.view(hidden_state.size(0), hidden_state.size(1), n_heads, head_dim)

            if self.verbose:
                print(f"Shape of QKV tensors before FlashAttention: {query.shape}, {key.shape}, {value.shape}")
                print(f"Dtype of QKV tensors: {query.dtype}, {key.dtype}, {value.dtype}")

            # Apply FlashAttention using positional arguments
            try:
                attn_output = flash_attn_func(query, key, value)  # Positional arguments only
                if self.verbose:
                    print(f"Shape of attention output: {attn_output.shape}")
                    print(f"Dtype of attention output: {attn_output.dtype}")
            except Exception as e:
                print(f"FlashAttention failed with error: {e}")
                raise

        # Mean pooling over the attention output
        # Convert attention output back to float32 if necessary
        embedding = attn_output.mean(dim=1).to(torch.float32).cpu().numpy().flatten()

        return embedding


if __name__ == "__main__":
    # Initialize CUDA-based memory class
    memory = CudaMemoryWithEmbeddings(forget_threshold=3, model_dir_index=1)

    # Test the memory class
    from agents.brain.memory.test import memory_tests
    memory_tests(memory)
