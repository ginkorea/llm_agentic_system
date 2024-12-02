import unittest
import subprocess
import sys

class TestMain(unittest.TestCase):

    def test_main_flow(self):
        cmd = [sys.executable, "main.py", "--category", "cs.CL", "--recent_days", "30", "--verbose"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertIn("Title:", result.stdout)

if __name__ == '__main__':
    unittest.main()