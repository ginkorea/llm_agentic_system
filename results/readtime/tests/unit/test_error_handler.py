import unittest
from workbench.readtime.error_handler import ErrorHandler

class TestErrorHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ErrorHandler()

    def test_handle_unsupported_format(self):
        with unittest.mock.patch('builtins.print') as mocked_print:
            self.handler.handle_unsupported_format("xml")
            mocked_print.assert_called_with("Error: Unsupported format 'xml'")

    def test_handle_invalid_input(self):
        with unittest.mock.patch('builtins.print') as mocked_print:
            self.handler.handle_invalid_input(None)
            mocked_print.assert_called_with("Error: Invalid input")

if __name__ == '__main__':
    unittest.main()