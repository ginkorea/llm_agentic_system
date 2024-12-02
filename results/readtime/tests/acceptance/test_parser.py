import unittest
from workbench.readtime.parser import ContentParser

class TestContentParser(unittest.TestCase):
    def setUp(self):
        self.parser = ContentParser()

    def test_parse_plain_text(self):
        content = "This is plain text."
        parsed_content = self.parser.parse_plain_text(content)
        self.assertEqual(parsed_content, content)

    def test_parse_unsupported_format(self):
        content = "<html><body>This is a sample content.</body></html>"
        with self.assertRaises(ValueError):
            self.parser.parse_content(content, "xml")

if __name__ == '__main__':
    unittest.main()