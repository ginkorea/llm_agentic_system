import unittest
from workbench.readtime.calculator import ReadTimeCalculator

class TestReadTimeCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = ReadTimeCalculator()

    def test_estimate_reading_time_plain_text(self):
        content = "This is a sample content for reading time estimation."
        format = "plain"
        wpm = 265
        reading_time = self.calculator.estimate_reading_time(content, format, wpm)
        self.assertAlmostEqual(reading_time, len(content.split()) / wpm)

    def test_estimate_reading_time_unsupported_format(self):
        content = "<html><body>This is a sample content.</body></html>"
        format = "xml"
        with self.assertRaises(ValueError):
            self.calculator.estimate_reading_time(content, format)

if __name__ == '__main__':
    unittest.main()