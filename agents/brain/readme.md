# Brain Module

The Brain module serves as the core decision-making and processing unit of the system. It is responsible for coordinating inputs, managing memory, invoking tools, and processing goals through modular lobes. Among the various implementations, the `CodeBrain` is the primary and fully implemented subclass, specifically designed for software development tasks based on structured inputs like PRDs, UML diagrams, and architectural designs.

![Brain Lobes Image](brain_lobe_image.png)

---

## Overview

The Brain module abstracts the workflow into several components:
- **Core Brain Functionality**: Provided by `core.py`, this serves as the foundational class for all Brain types.
- **Specialized Brains**: Includes `CodeBrain` for software development and `CognitiveBrain` for more abstract reasoning tasks.
- **Memory Management**: Incorporates multiple memory types (e.g., CUDA, OpenVINO, Embedded, and Simple).
- **Tool and Module Integration**: Provides a seamless interface for invoking tools and modules based on input requirements.

---

## Key Files and Their Functions

### 1. `core.py`
- **Purpose**: Provides the foundational functionality for the Brain class.
- **Features**:
  - **Memory Initialization**: Supports various memory types (`embedded`, `cuda`, `openvino`, and `simple`).
  - **Module Loading**: Dynamically loads lobes (modules) such as Control, Memory, and Main modules.
  - **Tool Integration**: Builds descriptions for tools and invokes them when needed.
  - **Goal and Milestone Handling**: Works with `Goal` objects to track and manage milestone progression.
  - **Action Determination**: Routes input to appropriate tools or modules based on goals or explicit actions.

### 2. `code_brain_model.py`
- **Purpose**: Extends `core.py` to handle software development tasks.
- **Features**:
  - **PRD, UML, and Architecture Parsing**: Processes structured inputs to guide software generation.
  - **Milestone Modules**: Links goals and milestones to specific lobes, ensuring task modularity.
  - **Custom Memory Context**: Leverages embedded or advanced memory models (e.g., CUDA) for task-specific recall.

### 3. `goal.py`
- **Purpose**: Manages high-level goals and milestone progression.
- **Features**:
  - Tracks progress across milestones.
  - Provides utility methods for progress visualization and updates.

### 4. `software_dev_goal.py`
- **Purpose**: Implements specific goals for software development workflows.
- **Features**:
  - Includes predefined milestones such as UML validation, code implementation, and test execution.
  - Leverages modular Brain capabilities to ensure tasks are logically sequenced.

---

## Features of `CodeBrain`

The `CodeBrain` is specifically designed to:
1. **Develop Software**: Leverages PRDs, UML diagrams, and architecture inputs to generate, validate, and refine code.
2. **Track Milestone Progress**: Updates progress based on `is_achieved` outputs from each milestone.
3. **Execute Tests**: Automatically generates, stores, and runs acceptance and unit tests.

---

## Workflow Example

### Initialization
```python
from agents.brain.code_brain_model import CodeBrain
from agents.toolkit.bag import BagOfTools

# Instantiate the brain
toolkit = BagOfTools()
toolkit.get_tools()
brain = CodeBrain(
    toolkit=toolkit,
    forget_threshold=10,
    verbose=True,
    memory_type='cuda',
    goal="Develop Python Package",
    goal_file="path/to/prd.md"
)
```

### Processing Input
```python
input_data = "Generate UML and validate the Architecture Design"
result, _, achieved, module = brain.process_input(input_data, chaining_mode=True)
```

### Milestone Handling
Milestones are tracked and managed within the Brain, which dynamically determines:
- If a milestone is achieved.
- Which module or tool is required for the next step.
- How to store intermediate outputs in memory.

---

## Extensibility

The Brain module is built for flexibility:
- **Custom Lobes**: Add new modules or lobes to extend functionality.
- **Toolkits**: Integrate additional tools for domain-specific tasks.
- **Memory Models**: Implement new memory classes for specialized contexts.

For detailed implementation examples, refer to `code_brain_model.py` or `core.py`.
