import pandas as pd
from workbench.chakin.word_vector import WordVector

class CSVHandler:
    def loadCSV(self, filePath: str) -> list:
        return pd.read_csv(filePath).to_dict('records')

    def parseCSV(self) -> list:
        data = self.loadCSV('./chakin/datasets.csv')
        return [WordVector(**row) for row in data]