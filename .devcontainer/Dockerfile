# Use an official Python 3.11 container image from Microsoft for DevContainers
FROM mcr.microsoft.com/devcontainers/python:0-3.11-bullseye

# Set the working directory inside the container
WORKDIR /workspace

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y git-lfs

# Ensure Git LFS is set up
RUN git lfs install

# Copy all project files to the working directory in the container
COPY . /workspace

# Install core dependencies from setup.py
RUN pip install --upgrade pip
RUN pip install .

# Expose a default port (if necessary, depending on your application)
EXPOSE 8080

# Default command to run when the container starts
CMD ["python", "main.py"]
