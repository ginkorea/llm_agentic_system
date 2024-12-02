import pandas as pd

class FinancialDataProcessor:
    def loadData(self, filePath: str) -> pd.DataFrame:
        """Load data from a CSV file."""
        return pd.read_csv(filePath)

    def preprocessData(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the data by normalizing column names."""
        data.columns = map(str.lower, data.columns)
        return data