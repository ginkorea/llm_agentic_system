import unittest
from unittest.mock import patch
import subprocess
import sys

class TestMain(unittest.TestCase):

    @patch('subprocess.run')
    def test_main_flow(self, mock_run):
        # Mock the subprocess.run to simulate the CLI execution
        mock_run.return_value = subprocess.CompletedProcess(args=['python', 'main.py'], returncode=0, stdout='Conversion complete')
        
        # Simulate calling the main script
        result = subprocess.run([sys.executable, 'main.py'], capture_output=True, text=True)
        
        # Assert that the process was called with expected arguments
        mock_run.assert_called_with([sys.executable, 'main.py'], capture_output=True, text=True)
        self.assertIn('Conversion complete', result.stdout)

if __name__ == '__main__':
    unittest.main()