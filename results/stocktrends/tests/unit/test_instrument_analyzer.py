import unittest
import pandas as pd
from workbench.financial_analysis.instrument_analyzer import InstrumentAnalyzer

class TestInstrumentAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = InstrumentAnalyzer()
        self.sample_data = pd.DataFrame({
            'date': ['2021-01-01', '2021-01-02'],
            'open': [100, 102],
            'high': [110, 112],
            'low': [90, 92],
            'close': [105, 107]
        })

    def test_analyze_instrument(self):
        analysis_result = self.analyzer.analyzeInstrument(self.sample_data, 'stock')
        self.assertIsInstance(analysis_result, dict)
        self.assertIn('analysis', analysis_result)

if __name__ == '__main__':
    unittest.main()