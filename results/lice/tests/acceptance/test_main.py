import unittest
import subprocess

class TestMain(unittest.TestCase):
    def test_main_execution(self):
        result = subprocess.run(['python', 'main.py'], capture_output=True, text=True)
        self.assertIn("Template Content for ExampleOrg in 2021 using Python", result.stdout)

if __name__ == "__main__":
    unittest.main()