from pydantic import BaseModel
import os
import subprocess
from langchain_core.tools import tool

# Input schema for running code in an existing virtual environment
class RunExistingVenvInput(BaseModel):
    file_path: str  # Path to the Python file to execute
    env_name: str = "env"
    arguments: list[str] = 'default_factory'  # Optional list of command-line arguments


@tool
def run_code_in_existing_virtualenv(input_data: RunExistingVenvInput) -> str:
    """
    Run a Python file in an existing virtual environment with optional arguments.

    Args:
        input_data (RunExistingVenvInput): Contains the file path, environment name, and optional arguments.

    Returns:
        str: Output of the code execution or error message.
    """
    try:
        file_path = input_data.file_path
        env_name = input_data.env_name
        arguments = input_data.arguments

        # Ensure the virtual environment exists
        if not os.path.exists(env_name):
            return f"Error: Virtual environment '{env_name}' does not exist."

        # Ensure the file exists
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."

        # Activate the virtual environment
        env_bin = os.path.join(env_name, "bin" if os.name != "nt" else "Scripts")
        python_executable = os.path.join(env_bin, "python")

        # Construct the command
        command = [python_executable, file_path] + arguments

        # Execute the command
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Return the output or error
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error:\n{result.stderr}"

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Example Usage: Run Code in Existing Virtual Environment
    run_input = RunExistingVenvInput(
        file_path="example_script.py",  # path to example Python file
        env_name="test_env",
        arguments=["--arg1", "value1", "--flag"]
    )
    run_result = run_code_in_existing_virtualenv.invoke({"input_data": run_input.dict()})
    print(run_result)
