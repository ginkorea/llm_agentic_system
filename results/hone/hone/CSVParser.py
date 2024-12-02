# CSVParser.py
import csv

class CSVParser:
    def parseCSV(self, filePath, delimiter):
        with open(filePath, mode='r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            return list(reader)

    def extractColumnNames(self, data):
        return data[0] if data else []

    def extractDataRows(self, data):
        return data[1:] if data else []