from pydantic import BaseModel
import os
import subprocess
import venv
from langchain_core.tools import tool
from agents.toolkit.run_code_in_virtual_environment import run_code_in_existing_virtualenv


# Input schema for creating virtual environment
class CreateVenvInput(BaseModel):
    env_name: str = "env"
    requirements_file: str


@tool
def create_virtualenv_with_requirements(input_data: CreateVenvInput) -> tuple[bool, str]:
    """
    Create a virtual environment and install dependencies from requirements.txt.

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

        # Ensure pip is installed
        env_bin = os.path.join(env_name, "bin" if os.name != "nt" else "Scripts")
        python_executable = os.path.join(env_bin, "python")
        pip_executable = os.path.join(env_bin, "pip")

        if not os.path.exists(pip_executable):
            subprocess.run([python_executable, "-m", "ensurepip"], check=True)
            subprocess.run([pip_executable, "install", "--upgrade", "pip"], check=True)

        # Install requirements from requirements.txt
        if os.path.exists(requirements_file):
            install_command = [pip_executable, "install", 'setuptools']
            subprocess.run(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            install_command = [pip_executable, "install", "-r", requirements_file]
            result = subprocess.run(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0:
                return False, f"Error installing requirements: {result.stderr}"

            return True, f"Virtual environment '{env_name}' created and requirements installed successfully."
        else:
            return False, "Error: Requirements file '{requirements_file}' not found."

    except Exception as e:
        return False, f"An error occurred: {e}"



if __name__ == "__main__":
    # Tool 1: Create Virtual Environment
    create_input = CreateVenvInput(
        env_name="test_env",
        requirements_file="requirements.txt"
    )
    passed, return_result = create_virtualenv_with_requirements.invoke({"input_data": create_input.model_dump()})
    print(passed)
    print(return_result)

