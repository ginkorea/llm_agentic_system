import unittest
from unittest.mock import mock_open, patch
from workbench.FileManager import FileManager

class TestFileManager(unittest.TestCase):

    def setUp(self):
        self.manager = FileManager()

    @patch('builtins.open', new_callable=mock_open, read_data='data')
    def test_openFile(self, mock_file):
        with self.manager.openFile('path/to/file', 'r') as f:
            result = f.read()
        mock_file.assert_called_with('path/to/file', 'r')
        self.assertEqual(result, 'data')

    @patch('builtins.open', new_callable=mock_open)
    def test_writeJSONToFile(self, mock_file):
        self.manager.writeJSONToFile('{"key": "value"}', 'path/to/output.json')
        mock_file.assert_called_with('path/to/output.json', 'w')
        mock_file().write.assert_called_once_with('{"key": "value"}')

if __name__ == '__main__':
    unittest.main()