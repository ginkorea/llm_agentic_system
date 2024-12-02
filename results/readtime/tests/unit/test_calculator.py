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

    def test_estimate_reading_time_html(self):
        content = "<p>This is a sample HTML content for reading time estimation.</p>"
        format = "html"
        # Assuming parse_html is implemented correctly
        with unittest.mock.patch('workbench.readtime.parser.ContentParser.parse_html', return_value="This is a sample HTML content for reading time estimation."):
            reading_time = self.calculator.estimate_reading_time(content, format)
            self.assertAlmostEqual(reading_time, len("This is a sample HTML content for reading time estimation.".split()) / 265)

    def test_estimate_reading_time_markdown(self):
        content = "# Sample Markdown\nThis is a sample markdown content."
        format = "markdown"
        # Assuming parse_markdown is implemented correctly
        with unittest.mock.patch('workbench.readtime.parser.ContentParser.parse_markdown', return_value="Sample Markdown This is a sample markdown content."):
            reading_time = self.calculator.estimate_reading_time(content, format)
            self.assertAlmostEqual(reading_time, len("Sample Markdown This is a sample markdown content.".split()) / 265)

    def test_estimate_reading_time_unsupported_format(self):
        content = "<xml>This is a sample content.</xml>"
        format = "xml"
        reading_time = self.calculator.estimate_reading_time(content, format)
        self.assertEqual(reading_time, 0)

if __name__ == '__main__':
    unittest.main()