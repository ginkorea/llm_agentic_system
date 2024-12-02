import unittest
from unittest.mock import patch
from workbench.main import main

class TestMain(unittest.TestCase):
    @patch('workbench.chakin.Chakin.search')
    @patch('workbench.chakin.Chakin.download')
    def test_main_flow(self, mock_download, mock_search):
        mock_search.return_value = ['Vector1']
        mock_download.return_value = True

        main()

        mock_search.assert_called_once_with(lang='English')
        mock_download.assert_called_once_with(index=0, saveDir='./')

if __name__ == '__main__':
    unittest.main()