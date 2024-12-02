from workbench.readtime.parser import ContentParser
from workbench.readtime.error_handler import ErrorHandler

class ReadTimeCalculator:
    def __init__(self):
        self.parser = ContentParser()
        self.error_handler = ErrorHandler()

    def estimate_reading_time(self, content, format, wpm=265):
        try:
            parsed_content = self.parser.parse_content(content, format)
            word_count = len(parsed_content.split())
            return word_count / wpm
        except Exception as e:
            self.error_handler.handle_invalid_input(content)
            return 0

    def validate_content(self, content, format):
        # Implementation of content validation
        pass