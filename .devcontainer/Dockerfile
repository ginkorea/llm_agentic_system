# Use Python 3.11 as the base image
FROM mcr.microsoft.com/devcontainers/python:0-3.11

# Set the working directory inside the container
WORKDIR /workspace

# Install system dependencies including Graphviz
RUN apt-get update && \
    apt-get install -y wget unzip gnupg2 graphviz && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+') && \
    wget -N https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Ensure Git LFS is set up
RUN apt-get install -y git-lfs && git lfs install

# Copy all project files to the working directory in the container
COPY . /workspace

# Install core dependencies from setup.py
RUN pip install --upgrade pip
RUN pip install .

# Expose a default port (if necessary)
EXPOSE 8080

# Default command to run when the container starts
CMD ["python", "main.py"]
