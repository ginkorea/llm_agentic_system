import unittest
import pandas as pd
from workbench.financial_analysis.test_validator import TestValidator

class TestTestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = TestValidator()
        self.sample_data = pd.DataFrame({
            'date': ['2021-01-01', '2021-01-02'],
            'close': [105, 107]
        })
        self.expected_data = pd.DataFrame({
            'date': ['2021-01-01', '2021-01-02'],
            'close': [105, 107]
        })

    def test_validate_indicators(self):
        is_valid = self.validator.validateIndicators(self.sample_data, self.expected_data)
        self.assertTrue(is_valid)

    def test_check_data_integrity(self):
        data_integrity = self.validator.checkDataIntegrity(self.sample_data)
        self.assertTrue(data_integrity)

if __name__ == '__main__':
    unittest.main()