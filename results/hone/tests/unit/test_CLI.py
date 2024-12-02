import unittest
import argparse
from unittest.mock import patch
from workbench.CLI import CLI

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.cli = CLI()

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(csv_filepath='input.csv', json_filepath='output.json', delimiter=','))
    def test_parseArguments(self, mock_args):
        args = self.cli.parseArguments()
        self.assertEqual(args.csv_filepath, 'input.csv')
        self.assertEqual(args.json_filepath, 'output.json')
        self.assertEqual(args.delimiter, ',')

    # Since executeConversion is a high-level integration, detailed testing would involve integration tests

if __name__ == '__main__':
    unittest.main()