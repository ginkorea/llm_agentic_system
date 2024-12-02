import unittest
from workbench.query_arxiv.query_params import QueryParams

class TestQueryParams(unittest.TestCase):

    def test_query_params_initialization(self):
        params = QueryParams(category="cs.CL", title="neural networks", author="Doe", abstract="learning", recent_days=30, max_results=5)
        self.assertEqual(params.category, "cs.CL")
        self.assertEqual(params.title, "neural networks")
        self.assertEqual(params.author, "Doe")
        self.assertEqual(params.abstract, "learning")
        self.assertEqual(params.recent_days, 30)
        self.assertEqual(params.max_results, 5)

if __name__ == '__main__':
    unittest.main()