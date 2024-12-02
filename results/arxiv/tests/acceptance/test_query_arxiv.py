import unittest
from workbench.query_arxiv.query_arxiv import QueryArXiv
from workbench.query_arxiv.query_params import QueryParams
from workbench.query_arxiv.paper import Paper

class TestQueryArXiv(unittest.TestCase):

    def setUp(self):
        self.query_arxiv = QueryArXiv()

    def test_execute_query(self):
        params = QueryParams(category="cs.CL", recent_days=30)
        papers = self.query_arxiv.executeQuery(params)
        self.assertIsInstance(papers, list)
        if papers:
            self.assertIsInstance(papers[0], Paper)

    def test_print_results(self):
        papers = [Paper("cs.CL", "Sample Title", "Author Name", "Sample Abstract", "2023-10-01", "http://arxiv.org/abs/1234")]
        self.query_arxiv.printResults(papers, verbose=True)

    def test_save_results_to_csv(self):
        papers = [Paper("cs.CL", "Sample Title", "Author Name", "Sample Abstract", "2023-10-01", "http://arxiv.org/abs/1234")]
        self.query_arxiv.saveResultsToCSV(papers, "test_output.csv")

if __name__ == '__main__':
    unittest.main()