import unittest
from workbench.query_arxiv.xml_parser import XMLParser
from workbench.query_arxiv.paper import Paper

class TestXMLParser(unittest.TestCase):

    def test_parse(self):
        xml_data = """
        <feed>
            <entry>
                <category term="cs.CL"/>
                <title>Sample Title</title>
                <author><name>Author Name</name></author>
                <summary>Sample Abstract</summary>
                <published>2023-10-01</published>
                <id>http://arxiv.org/abs/1234</id>
            </entry>
        </feed>
        """
        parser = XMLParser()
        papers = parser.parse(xml_data)
        self.assertEqual(len(papers), 1)
        self.assertIsInstance(papers[0], Paper)

if __name__ == '__main__':
    unittest.main()