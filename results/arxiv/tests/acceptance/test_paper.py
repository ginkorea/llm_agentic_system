import unittest
from workbench.query_arxiv.paper import Paper

class TestPaper(unittest.TestCase):

    def test_paper_initialization(self):
        paper = Paper("cs.CL", "Sample Title", "Author Name", "Sample Abstract", "2023-10-01", "http://arxiv.org/abs/1234")
        self.assertEqual(paper.category, "cs.CL")
        self.assertEqual(paper.title, "Sample Title")
        self.assertEqual(paper.author, "Author Name")
        self.assertEqual(paper.abstract, "Sample Abstract")
        self.assertEqual(paper.published, "2023-10-01")
        self.assertEqual(paper.link, "http://arxiv.org/abs/1234")

if __name__ == '__main__':
    unittest.main()