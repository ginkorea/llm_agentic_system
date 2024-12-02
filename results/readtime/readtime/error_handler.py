class ErrorHandler:
    def handle_unsupported_format(self, format):
        print(f"Error: Unsupported format '{format}'")

    def handle_invalid_input(self, content):
        print("Error: Invalid input")