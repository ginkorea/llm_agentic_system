import os

class Models:

    def __init__(self):
        self.model_directories = self.get_model_dir()
        self.tokenizers = self.get_tokenizers()
        self.dict = zip(self.tokenizers, self.model_directories)


    @staticmethod
    def get_tokenizers():
        tokenizers = ["model/jina-embeddings-v3/", "model/graphcodebert-base/", 'model/graphcodebert-py/']
        return tokenizers

    @staticmethod
    def get_model_dir():
        """
        Function to return the absolute paths of all subdirectories in the directory where this script is located.

        :return: A list of absolute paths for all subdirectories in the directory where this script is located.
        """
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        model_dirs = []

        # Loop through the entries in the script's directory
        for entry in os.listdir(script_dir):
            entry_path = os.path.join(script_dir, entry)
            # Check if the entry is a directory
            if os.path.isdir(entry_path) and not entry.startswith("__"):
                # Append the absolute path of the directory
                model_dirs.append(os.path.abspath(entry_path))

        return model_dirs


# Example usage:
if __name__ == "__main__":
    models = Models()

    for tokenizer, model_dir in models.dict:
        print(f"Tokenizer: {tokenizer}, Model Directory: {model_dir}")
