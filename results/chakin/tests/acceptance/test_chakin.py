import unittest
from unittest.mock import patch, MagicMock
from workbench.chakin.chakin import Chakin

class TestChakin(unittest.TestCase):
    def setUp(self):
        self.chakin = Chakin()

    @patch('workbench.chakin.csv_handler.CSVHandler.parseCSV')
    def test_search(self, mock_parseCSV):
        mock_parseCSV.return_value = [
            MagicMock(language='English'),
            MagicMock(language='Spanish')
        ]
        results = self.chakin.search(lang='English')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].language, 'English')

    @patch('workbench.chakin.csv_handler.CSVHandler.parseCSV')
    @patch('workbench.chakin.progress_bar.ProgressBar.start')
    @patch('workbench.chakin.progress_bar.ProgressBar.update')
    @patch('workbench.chakin.progress_bar.ProgressBar.finish')
    def test_download(self, mock_finish, mock_update, mock_start, mock_parseCSV):
        mock_parseCSV.return_value = [
            MagicMock(name='Vector1', language='English'),
            MagicMock(name='Vector2', language='Spanish')
        ]
        result = self.chakin.download(index=0, saveDir='./')
        self.assertTrue(result)
        mock_start.assert_called_once()
        mock_update.assert_called()
        mock_finish.assert_called_once()

if __name__ == '__main__':
    unittest.main()