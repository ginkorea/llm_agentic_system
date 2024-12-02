import unittest
from unittest.mock import patch
from workbench.query_arxiv.arxiv_api import ArXivAPI
from workbench.query_arxiv.query_params import QueryParams

class TestArXivAPI(unittest.TestCase):

    @patch('workbench.query_arxiv.arxiv_api.requests.get')
    def test_fetch_data(self, mock_get):
        mock_get.return_value.content = "<xml></xml>"
        api = ArXivAPI()
        params = QueryParams(category="cs.CL", recent_days=30)
        response = api.fetchData(params)
        self.assertEqual(response, "<xml></xml>")

if __name__ == '__main__':
    unittest.main()