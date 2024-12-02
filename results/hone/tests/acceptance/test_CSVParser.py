import unittest
from results.hone.hone.CSVParser import CSVParser

class TestCSVParser(unittest.TestCase):

    def setUp(self):
        self.parser = CSVParser()
        self.sample_data = [
            ["name", "age", "city"],
            ["Alice", "30", "New York"],
            ["Bob", "25", "Los Angeles"]
        ]

    def test_parseCSV(self):
        # This test would normally read from a file, but here we simulate the data
        expected_data = self.sample_data
        parsed_data = self.parser.parseCSV('path/to/sample.csv', ',')
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