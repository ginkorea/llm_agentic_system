from pydantic import BaseModel
import os
import subprocess
from langchain_core.tools import tool

# Input schema for running code in an existing virtual environment
class RunExistingVenvInput(BaseModel):
    file_path: str  # Path to the Python file to execute
    env_name: str = "env"
    arguments: list[str] = 'default_factory'  # Optional list of command-line arguments

class CodeRunner:
    """
    A wrapper class for running Python files in existing virtual environments, does not set up the virtual environment.
    """

    def __init__(self, env_name="env"):
        self.env_name = env_name

    def run(self, file_path: str, arguments: list[str] = None) -> str:
        """
        Run a Python file in the configured virtual environment.

        Args:
            file_path (str): Path to the Python file.
            arguments (list[str]): Optional list of command-line arguments.

        Returns:
            str: Output of the code execution or error message.
        """
        if arguments is None:
            arguments = []

        input_data = RunExistingVenvInput(file_path=file_path, env_name=self.env_name, arguments=arguments)
        return run_code_in_existing_virtualenv.invoke({"input_data": input_data.model_dump()})


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
    # Initialize the CodeRunner
    code_runner = CodeRunner(env_name="test_env")

    # Run an example script
    result = code_runner.run(
        file_path="example_script.py",  # Path to the Python file to execute
        arguments=["--arg1", "value1", "--flag"]
    )

    print(result)
