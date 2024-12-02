import unittest
from unittest.mock import patch
from workbench.main import main

class TestMainFlow(unittest.TestCase):
    @patch('builtins.print')
    def test_main_flow(self, mock_print):
        main()
        mock_print.assert_called_with("Estimated Reading Time: 0.0 minutes")

if __name__ == '__main__':
    unittest.main()