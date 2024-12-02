import unittest
from workbench.CSVParser import CSVParser

class TestCSVParser(unittest.TestCase):

    def setUp(self):
        self.parser = CSVParser()
        self.sample_data = [
            ["name", "age", "city"],
            ["Alice", "30", "New York"],
            ["Bob", "25", "Los Angeles"]
        ]

    def test_parseCSV(self):
        # Mocking file reading instead of actual file I/O
        with unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data='name,age,city\nAlice,30,New York\nBob,25,Los Angeles')):
            parsed_data = self.parser.parseCSV('dummy_path.csv', ',')
            expected_data = self.sample_data
            self.assertEqual(parsed_data, expected_data)

    def test_extractColumnNames(self):
        expected_columns = ["name", "age", "city"]
        columns = self.parser.extractColumnNames(self.sample_data)
        self.assertEqual(columns, expected_columns)

    def test_extractDataRows(self):
        expected_rows = [
            ["Alice", "30", "New York"],
            ["Bob", "25", "Los Angeles"]
        ]
        rows = self.parser.extractDataRows(self.sample_data)
        self.assertEqual(rows, expected_rows)

if __name__ == '__main__':
    unittest.main()