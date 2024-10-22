# Use Python 3.11 as the base image
FROM mcr.microsoft.com/devcontainers/python:0-3.11

# Set the working directory inside the container
WORKDIR /workspace

# Install system dependencies including Graphviz
RUN apt-get update && apt-get install -y git-lfs graphviz

# Ensure Git LFS is set up
RUN git lfs install

# Copy all project files to the working directory in the container
COPY . /workspace

# Install core dependencies from setup.py
RUN pip install --upgrade pip
RUN pip install .

# Expose a default port (if necessary)
EXPOSE 8080

# Default command to run when the container starts
CMD ["python", "main.py"]
