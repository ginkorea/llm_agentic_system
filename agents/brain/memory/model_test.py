import numpy as np
from transformers import AutoTokenizer
from openvino.runtime import Core

# Initialize OpenVINO runtime
ie = Core()

# Load the FP16 model
model = ie.read_model(model="model_onnx/model_fp16.onnx")
compiled_model = ie.compile_model(model=model, device_name="CPU")

# Check the input/output of the model
print(compiled_model.inputs)
print(compiled_model.outputs)

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v3")

# Tokenize the input text (replace "your input text here" with actual text)
inputs = tokenizer("your input text here", return_tensors="np")

# Prepare input data (convert to numpy arrays)
input_ids = inputs["input_ids"].astype(np.int64)
attention_mask = inputs["attention_mask"].astype(np.int64)
task_id = np.array(0, dtype=np.int64)  # Example task ID, if needed

# Run inference (pass the inputs as a list of numpy arrays)
input_data = [input_ids, attention_mask, task_id]
results = compiled_model(input_data)

# Output the results
output_layer = compiled_model.output(0)
print(results[output_layer])
