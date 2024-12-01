import os
import shutil
import logging


class Cleaner:
    def __init__(self):
        self.workbench = "workbench"
        self.env = "project_env"

    def clean_space(self, directory: str, add_init: bool = True):
        """
        Clean the specified directory by removing all files and subdirectories.
        Optionally, add an __init__.py file to the directory.

        Args:
            directory (str): Path to the directory to clean.
            add_init (bool): Add an __init__.py file to the directory (default: True).
        """
        try:
            # Ensure the directory exists
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Remove all files and subdirectories
            for root, dirs, files in os.walk(directory, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    os.remove(file_path)
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    os.rmdir(dir_path)

            # Create a new __init__.py file if needed
            if add_init:
                self.add_init_file(directory)

            logging.info(f"Directory '{directory}' cleaned and initialized.")
        except Exception as e:
            logging.error(f"Error cleaning directory '{directory}': {e}")

    @staticmethod
    def add_init_file(directory: str):
        """
        Add an __init__.py file to the specified directory.

        Args:
            directory (str): Path to the directory.
        """
        try:
            init_file_path = os.path.join(directory, "__init__.py")
            with open(init_file_path, "w") as init_file:
                init_file.write("# Package initialization\n")

            logging.info(f"Added __init__.py file to '{directory}'.")
        except Exception as e:
            logging.error(f"Error adding __init__.py to '{directory}': {e}")

    def start_fresh(self):
        """
        Reset the workbench and environment directories by cleaning them.
        Deletes the virtual environment if it exists and recreates the workbench.

        Args:
            None
        """
        try:
            # Clean the workbench directory
            self.clean_space(self.workbench)

            # Remove and recreate the virtual environment directory
            if os.path.exists(self.env):
                shutil.rmtree(self.env)
                logging.info(f"Removed existing virtual environment: '{self.env}'.")

        except Exception as e:
            logging.error(f"Error resetting workspace: {e}")


# Example Usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Initialize Cleaner
    cleaner = Cleaner()


    # Start fresh by resetting workbench and environment
    cleaner.start_fresh()
