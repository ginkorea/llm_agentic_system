# CLI.py
import argparse
from results.hone.hone.CSVParser import CSVParser
from results.hone.hone.JSONGenerator import JSONGenerator
from results.hone.hone.FileManager import FileManager

class CLI:
    def parseArguments(self):
        parser = argparse.ArgumentParser(description='CSV to JSON Converter')
        parser.add_argument('csv_filepath', type=str, help='Path to the input CSV file')
        parser.add_argument('json_filepath', type=str, help='Path to the output JSON file')
        parser.add_argument('--delimiter', type=str, default=',', help='CSV delimiter')
        return parser.parse_args()

    def executeConversion(self, args):
        csv_parser = CSVParser()
        data = csv_parser.parseCSV(args.csv_filepath, args.delimiter)
        column_names = csv_parser.extractColumnNames(data)
        data_rows = csv_parser.extractDataRows(data)

        json_generator = JSONGenerator()
        schema = json_generator.generateSchema(column_names)
        json_data = json_generator.convertToJSON(data_rows, schema)

        file_manager = FileManager()
        file_manager.writeJSONToFile(json_data, args.json_filepath)