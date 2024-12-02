import unittest
from workbench.financial_analysis.report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ReportGenerator()

    def test_generate_report(self):
        analysis_result = {"analysis": "result"}
        report = self.generator.generateReport(analysis_result)
        self.assertIsInstance(report, str)

if __name__ == '__main__':
    unittest.main()