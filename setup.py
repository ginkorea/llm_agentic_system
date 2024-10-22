from setuptools import setup, find_packages

# Read the contents of your README file (optional, for detailed descriptions)
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LLM Agentic System for Software Development",  # Replace with your project name
    version="0.1",  # Your project version
    author="Josh Gompert, Nathan Smith, and Kruti Shah",
    description="Autonomous Software Development System using LLM-based agents",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Optional if using README.md
    url="https://github.com/ginkorea/llm_agentic_system",  # Link to your repository
    packages=find_packages(),  # Automatically find your project packages
    install_requires=[
        "langchain-openai~=0.2.0",
        "langchain~=0.3.0",
        "requests~=2.32.3",
        "selenium~=4.24.0",
        "beautifulsoup4~=4.12.3",
        "langchain-core~=0.3.1",
        "numpy~=1.26.4",
        "scikit-learn~=1.5.2",
        "openvino~=2024.4.0",
        "transformers~=4.44.2",
        "graphviz~=0.20.3",
        "pandas~=2.2.3",
        "tqdm~=4.66.5",
        "openai~=1.46.0",
        "setuptools~=75.1.0",
        "tenacity~=8.5.0",
        "colorama~=0.4.6",
        "tiktoken~=0.7.0",
        "six~=1.16.0",
        "datasets~=3.0.1",
        "evaluate~=0.4.3",
        "lxml~=5.3.0",
        "opencv-python~=4.10.0.84",
        "rich~=13.9.2",
        "portalocker~=2.10.1",
        "pydantic~=2.8.2",
        "torch~=2.5.0",
        "progressbar2~=3.53.2",
    ],
    extras_require={
        "gpu": ["flash_attn~=2.6.3"],  # Optional dependency for GPU users
    },
    python_requires='>=3.10',  # Ensure the correct Python version
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your license
        "Operating System :: OS Independent",
    ],
)
