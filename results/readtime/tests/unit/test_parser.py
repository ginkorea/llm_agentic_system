import unittest
from workbench.readtime.parser import ContentParser

class TestContentParser(unittest.TestCase):
    def setUp(self):
        self.parser = ContentParser()

    def test_parse_plain_text(self):
        content = "This is plain text."
        parsed_content = self.parser.parse_plain_text(content)
        self.assertEqual(parsed_content, content)

    def test_parse_html(self):
        content = "<p>This is a paragraph.</p>"
        # Assuming parse_html is implemented
        with unittest.mock.patch('workbench.readtime.parser.ContentParser.parse_html', return_value="This is a paragraph."):
            parsed_content = self.parser.parse_html(content)
            self.assertEqual(parsed_content, "This is a paragraph.")

    def test_parse_markdown(self):
        content = "# Heading\nThis is markdown."
        # Assuming parse_markdown is implemented
        with unittest.mock.patch('workbench.readtime.parser.ContentParser.parse_markdown', return_value="Heading This is markdown."):
            parsed_content = self.parser.parse_markdown(content)
            self.assertEqual(parsed_content, "Heading This is markdown.")

    def test_parse_unsupported_format(self):
        content = "<xml>This is unsupported format.</xml>"
        with self.assertRaises(ValueError):
            self.parser.parse_content(content, "xml")

if __name__ == '__main__':
    unittest.main()