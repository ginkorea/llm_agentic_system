import unittest
from unittest.mock import patch
from workbench.chakin.csv_handler import CSVHandler

class TestCSVHandler(unittest.TestCase):
    @patch('workbench.chakin.csv_handler.pd.read_csv')
    def test_loadCSV(self, mock_read_csv):
        mock_read_csv.return_value = [{'name': 'Vector1'}, {'name': 'Vector2'}]
        handler = CSVHandler()
        data = handler.loadCSV('dummy_path')
        self.assertEqual(len(data), 2)

    @patch('workbench.chakin.csv_handler.CSVHandler.loadCSV')
    def test_parseCSV(self, mock_loadCSV):
        mock_loadCSV.return_value = [
            {'name': 'Vector1', 'dimension': 300, 'corpus': 'Wikipedia', 'vocabulary_size': 1000000,
             'method': 'fastText', 'language': 'English', 'paper': 'Some Paper', 'author': 'Some Author',
             'url': 'http://example.com'}
        ]
        handler = CSVHandler()
        vectors = handler.parseCSV()
        self.assertEqual(len(vectors), 1)
        self.assertEqual(vectors[0].name, 'Vector1')

if __name__ == '__main__':
    unittest.main()