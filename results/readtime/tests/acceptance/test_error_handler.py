import unittest
from workbench.readtime.error_handler import ErrorHandler

class TestErrorHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ErrorHandler()

    def test_handle_unsupported_format(self):
        with self.assertRaises(ValueError):
            self.handler.handle_unsupported_format("xml")

    def test_handle_invalid_input(self):
        # Assuming handle_invalid_input raises an exception for invalid input
        with self.assertRaises(ValueError):
            self.handler.handle_invalid_input(None)

if __name__ == '__main__':
    unittest.main()