import unittest
from workbench.financial_analysis.data_processor import FinancialDataProcessor
from workbench.financial_analysis.indicator_calculator import IndicatorCalculator
from workbench.financial_analysis.instrument_analyzer import InstrumentAnalyzer
from workbench.financial_analysis.report_generator import ReportGenerator
from workbench.financial_analysis.test_validator import TestValidator

class TestMainFlow(unittest.TestCase):
    def setUp(self):
        self.processor = FinancialDataProcessor()
        self.calculator = IndicatorCalculator()
        self.analyzer = InstrumentAnalyzer()
        self.generator = ReportGenerator()
        self.validator = TestValidator()
        self.sample_data = pd.DataFrame({
            'date': ['2021-01-01', '2021-01-02'],
            'open': [100, 102],
            'high': [110, 112],
            'low': [90, 92],
            'close': [105, 107]
        })

    def test_main_flow(self):
        # Load and preprocess data
        preprocessed_data = self.processor.preprocessData(self.sample_data)

        # Calculate indicators
        renko_data = self.calculator.calculateRenko(preprocessed_data, 2.0, 'PERIOD_CLOSE')
        linebreak_data = self.calculator.calculateLineBreak(preprocessed_data, 3)
        pnf_data = self.calculator.calculatePnF(preprocessed_data)

        # Analyze instruments
        analysis_result = self.analyzer.analyzeInstrument(preprocessed_data, 'stock')

        # Generate report
        report = self.generator.generateReport(analysis_result)

        # Validate results
        is_valid = self.validator.validateIndicators(renko_data, preprocessed_data)
        data_integrity = self.validator.checkDataIntegrity(preprocessed_data)

        self.assertIsInstance(report, str)
        self.assertTrue(is_valid)
        self.assertTrue(data_integrity)

if __name__ == '__main__':
    unittest.main()