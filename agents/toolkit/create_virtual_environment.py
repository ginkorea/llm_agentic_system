from pydantic import BaseModel
import os
import subprocess
import venv
from langchain_core.tools import tool


# Input schema for creating virtual environment
class CreateVenvInput(BaseModel):
    env_name: str = "env"
    requirements_file: str


@tool
def create_virtualenv_with_requirements(input_data: CreateVenvInput) -> str:
    """
    Create a virtual environment and install dependencies from requirements.txt, not used for creating a requirements file.

    Args:
        input_data (CreateVenvInput): Contains the environment name and path to requirements.txt.

    Returns:
        str: Success or error message.
    """
    try:
        env_name = input_data.env_name
        requirements_file = input_data.requirements_file

        # Create the virtual environment
        if not os.path.exists(env_name):
            venv.create(env_name, with_pip=True)

        # Activate the virtual environment
        env_bin = os.path.join(env_name, "bin" if os.name != "nt" else "Scripts")
        pip_executable = os.path.join(env_bin, "pip")

        # Install requirements from requirements.txt
        if os.path.exists(requirements_file):
            subprocess.run([pip_executable, "install", "-r", requirements_file], check=True)
        else:
            return f"Error: Requirements file '{requirements_file}' not found."

        return f"Virtual environment '{env_name}' created and requirements installed successfully."

    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    # Tool 1: Create Virtual Environment
    create_input = CreateVenvInput(
        env_name="test_env",
        requirements_file="requirements.txt"
    )
    create_result = create_virtualenv_with_requirements.invoke({"input_data": create_input.dict()})
    print(create_result)

