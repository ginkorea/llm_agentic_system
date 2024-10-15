# Autonomous Software Development System

## Overview

This project is focused on building an **autonomous software development system** using **LLM-based agents** and a **multi-lobe architecture**. The system handles the entire software development lifecycle, including:
- **Planning**
- **Coding**
- **Testing**
- **Reviewing**

By using **hybrid memory structures** and **CUDA acceleration**, the system aims to improve memory management, computational efficiency, and the ability to refine past work through **file embeddings**.

## Key Features

- **Multi-Lobe Framework**: Specialized modules handle distinct tasks such as memory recall, reasoning, and problem-solving.
- **Hybrid Memory**: Efficient long-term and short-term memory management with file embedding.
- **Submodule Task Handling**: Modular components streamline tasks like code generation, testing, and environment setup.
- **CUDA Acceleration**: Boosts performance in memory retrieval and embedding operations.

## Project Structure

```
agents/
    brain/
        memory/
            model/
toolkit/
    visualize_file_structure.py
const/
main.py
requirements.txt
```

## Technologies

- **LangChain** and **OpenAI API** for LLM orchestration.
- **Jina AI** for embedding-based memory.
- **Python** as the primary development language.

## Work in Progress

This project is in active development and will evolve as new features are implemented and optimized. It is being tested using the **DevBench** benchmark for autonomous software development tasks.
