import unittest
from workbench.lice.language_detector import LanguageDetector

class TestLanguageDetector(unittest.TestCase):
    def setUp(self):
        self.detector = LanguageDetector()

    def test_detect_language(self):
        language = self.detector.detectLanguage('py')
        self.assertEqual(language, "Python")

    def test_detect_unknown_language(self):
        language = self.detector.detectLanguage('unknown')
        # Assuming the default return for unknown languages is "Unknown"
        self.assertEqual(language, "Unknown")

if __name__ == "__main__":
    unittest.main()