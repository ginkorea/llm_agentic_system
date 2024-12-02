import unittest
import subprocess
import sys

class TestMainFlow(unittest.TestCase):
    def test_training_flow(self):
        # Simulate running the training script
        cmd = [sys.executable, "workbench/main.py", "--train"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertIn("Training complete", result.stdout)

    def test_testing_flow(self):
        # Simulate running the testing script
        cmd = [sys.executable, "workbench/main.py", "--test"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertIn("Testing complete", result.stdout)

if __name__ == '__main__':
    unittest.main()