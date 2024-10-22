# Autonomous Software Development System

## Overview

This project focuses on building an **autonomous software development system** using **LLM-based agents** and a **multi-lobe architecture**. The system manages the entire software development lifecycle, including:
- **Planning**
- **Coding**
- **Testing**
- **Reviewing**

Using **hybrid memory structures** and **CUDA acceleration**, the system improves memory management, computational efficiency, and the ability to refine past work through **file embeddings**.

## Key Features

- **Multi-Lobe Framework**: Specialized modules handle distinct tasks such as memory recall, reasoning, and problem-solving.
- **Hybrid Memory**: Efficient long-term and short-term memory management with file embedding.
- **Submodule Task Handling**: Modular components streamline tasks like code generation, testing, and environment setup.
- **CUDA Acceleration**: Boosts performance in memory retrieval and embedding operations.

## Project Structure

```
agents/
    __init__.py
    base.py
    brain/
        __init__.py
        build_prompt.py
        core.py
        examples.py
        hippocampus.py
        lobes.py
        memory/
            __init__.py
            cuda_embedded.py
            embedded.py
            file_structure/
                graph
                graph.pdf
                tree.txt
            model/
                __init__.py
                get.py
                graphcodebert-base/
                graphcodebert-py/
                jina-embeddings-v3/
            model_test.py
            ov_embedded.py
            simple.py
            test.py
    toolkit/
        __init__.py
        bag.py
        calculate.py
        get_page.py
        search.py
        t.py
        to_upper.py
        visualize_file_structure.py
const/
    __init__.py
    _sk.py
    sk.py
main.py
readme.md
requirements.txt
```

## Technologies

- **LangChain** and **OpenAI API** for LLM orchestration.
- **Jina AI** for embedding-based memory.
- **Python** as the primary development language.
- **Torch and Triton** for high-performance computation on GPU.
- **OpenVINO** for hardware-accelerated inference.

### Installation Instructions

### Prerequisites

1. **Git with LFS (Large File Storage)**

   Make sure you have Git and Git LFS installed to clone the repository. Git LFS is required to handle large model files.
   
   **Install Git LFS**:
   - On Linux:
     ```bash
     sudo <your_package_manager> install git-lfs
     git lfs install
     ```
   - On macOS:
     ```bash
     brew install git-lfs
     git lfs install
     ```
   - On Windows, use the [Git LFS installer](https://git-lfs.github.com/).

2. **Python 3.10+**

   Ensure Python 3.10 or later is installed. You can check your Python version with:

   ```bash
   python --version
   ```

### Clone the Repository

```bash
git clone https://github.com/ginkorea/llm_agentic_system.git
cd llm_agentic_system
```

### Install the Dependencies Using `setup.py`

Instead of manually installing dependencies via `requirements.txt`, you can now install the package with the following command:

1. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install the package** (Core dependencies):

   ```bash
   pip install .
   ```

3. **Install optional GPU dependencies (FlashAttention)**:

   If you want to install FlashAttention for GPU acceleration, use the following command:

   ```bash
   pip install .[gpu, ov] # for CUDA [gpu] and OpenVINO [ov] acceleration
   ```

## API Key Configuration

This project requires API keys to access certain functionalities. To set up your API keys, follow these steps:

1. **Locate the API Key Example**:
   You will find an example API key file named `const/_sk.py`. This file contains placeholders for the required keys.

   Example structure of `const/_sk.py`:

   ```python
   import os

   class KeyChain:
       def __init__(self):
           self.open_ai = "your_openai_key"  # Replace with your OpenAI API key
           self.google_json = "your_google_json"  # Replace with your Google JSON key
           self.google_cx = "your_google_cx"  # Replace with your Google CX

   kc = KeyChain()
   os.environ["OPENAI_API_KEY"] = kc.open_ai


### Additional Setup for CUDA or OpenVINO

Depending on your hardware configuration, you may want to adjust the memory configuration:
- **CUDA**: If you're using NVIDIA GPUs, the system can utilize CUDA for fast computations with models.
- **OpenVINO**: For systems using Intel hardware, OpenVINO can accelerate ONNX models.



### Running the System

Once the setup is complete, you can start the system:

```bash
python main.py
```

The system will initialize the **autonomous agent** that can plan, code, and refine software projects autonomously.

## Tools Available

This project includes a set of integrated tools based off of the LangChain tools suite are available for the agent to use for various tasks:

1. **`calculate`**: 
   - Description: Evaluates mathematical expressions.
   - Usage: `calculate("2 + 2")`
   - Example Output: `4`

2. **`get_page`**:
   - Description: Retrieves the full text of a web page from a given URL.
   - Usage: `get_page("https://example.com")`
   - Example Output: The content of the web page as text.

3. **`search`**:
   - Description: Performs a Google search using Google's JSON API and returns top non-visited results.
   - Usage: `search({"query": "Python programming", "n_sites": 3, "visited_sites": []})`
   - Example Output: A list of search results containing titles, links, and snippets.

4. **`visualize_file_structure`**:
   - Description: Recursively builds a graph and text-based tree of the file structure, using colored submodules.
   - Usage: `visualize_file_structure(start_path=".")`
   - Example Output: A PDF of the file structure and a text-based tree.

5. **`BagOfTools`**:
   - Description: A class to manage and dynamically bind the above tools for flexible use.
   - Example Usage: You can call `get_tools()` to see a list of all available tools.

## Visualization of File Structures

You can also use the `visualize_file_structure.py` tool to generate visual representations of the file structure, outputting both a graph and a text-based tree.

