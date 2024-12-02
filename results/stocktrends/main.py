from workbench.financial_analysis.data_processor import FinancialDataProcessor
from workbench.financial_analysis.indicator_calculator import IndicatorCalculator
from workbench.financial_analysis.instrument_analyzer import InstrumentAnalyzer
from workbench.financial_analysis.report_generator import ReportGenerator
from workbench.financial_analysis.test_validator import TestValidator

if __name__ == "__main__":
    # Example usage of the classes
    processor = FinancialDataProcessor()
    calculator = IndicatorCalculator()
    analyzer = InstrumentAnalyzer()
    generator = ReportGenerator()
    validator = TestValidator()

    # Load and preprocess data
    data = processor.loadData('data/sample.csv')
    preprocessed_data = processor.preprocessData(data)

    # Calculate indicators
    renko_data = calculator.calculateRenko(preprocessed_data, 2.0, 'PERIOD_CLOSE')
    linebreak_data = calculator.calculateLineBreak(preprocessed_data, 3)
    pnf_data = calculator.calculatePnF(preprocessed_data)

    # Analyze instruments
    analysis_result = analyzer.analyzeInstrument(preprocessed_data, 'stock')

    # Generate report
    report = generator.generateReport(analysis_result)

    # Validate results
    is_valid = validator.validateIndicators(renko_data, preprocessed_data)
    data_integrity = validator.checkDataIntegrity(preprocessed_data)

    print(report)
    print(f"Validation: {is_valid}, Data Integrity: {data_integrity}")