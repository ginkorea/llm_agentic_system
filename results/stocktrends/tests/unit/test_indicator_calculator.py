import unittest
import pandas as pd
from workbench.financial_analysis.indicator_calculator import IndicatorCalculator

class TestIndicatorCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = IndicatorCalculator()
        self.sample_data = pd.DataFrame({
            'date': ['2021-01-01', '2021-01-02'],
            'open': [100, 102],
            'high': [110, 112],
            'low': [90, 92],
            'close': [105, 107]
        })

    def test_calculate_renko(self):
        renko_data = self.calculator.calculateRenko(self.sample_data, 2.0, 'PERIOD_CLOSE')
        self.assertIsInstance(renko_data, pd.DataFrame)

    def test_calculate_line_break(self):
        linebreak_data = self.calculator.calculateLineBreak(self.sample_data, 3)
        self.assertIsInstance(linebreak_data, pd.DataFrame)

    def test_calculate_pnf(self):
        pnf_data = self.calculator.calculatePnF(self.sample_data)
        self.assertIsInstance(pnf_data, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()