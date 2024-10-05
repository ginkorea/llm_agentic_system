from huggingface_hub import snapshot_download

# Download the ONNX model from Hugging Face
model_dir = snapshot_download(repo_id="sentence-transformers/paraphrase-MiniLM-L6-v2-onnx", revision="main")

print(f"Model downloaded to: {model_dir}")
