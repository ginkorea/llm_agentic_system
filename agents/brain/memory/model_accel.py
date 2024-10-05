import numpy as np
from openvino.runtime import Core

# Initialize OpenVINO runtime
ie = Core()

# Load the model
model_path = "/agents/brain/memory/model_ir/model.xml"
model = ie.read_model(model=model_path)

# Compile the model
compiled_model = ie.compile_model(model=model, device_name="CPU")  # Change to NPU if needed

# Prepare input data
# Ensure the input is a 1D tensor with 4 values (matching the expected [1, 4] shape)
input_data = np.random.randn(1, 4).astype(np.float32)

# Perform inference
results = compiled_model([input_data])

# Process results
print("Inference results:", results)
