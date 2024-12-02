import pandas as pd
from workbench.chakin.csv_handler import CSVHandler
from workbench.chakin.progress_bar import ProgressBar

class Chakin:
    def __init__(self):
        self.csv_handler = CSVHandler()
        self.progress_bar = ProgressBar()

    def search(self, lang: str) -> list:
        word_vectors = self.csv_handler.parseCSV()
        return [wv for wv in word_vectors if wv.language == lang]

    def download(self, index: int, saveDir: str) -> bool:
        word_vectors = self.csv_handler.parseCSV()
        if index < 0 or index >= len(word_vectors):
            print("Invalid index")
            return False

        vector = word_vectors[index]
        print(f"Downloading {vector.name} to {saveDir}")
        self.progress_bar.start()
        # Simulate download with progress
        for i in range(100):
            self.progress_bar.update(i / 100)
        self.progress_bar.finish()
        print("Download complete")
        return True