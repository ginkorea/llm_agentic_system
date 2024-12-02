import unittest
from workbench.textcnn_project.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()

    def test_load_dataset(self):
        dataset = self.processor.load_dataset()
        self.assertIn('train', dataset)
        self.assertIn('test', dataset)

    def test_preprocess_data(self):
        dataset = self.processor.load_dataset()
        train_dataset, test_dataset = self.processor.preprocess_data(dataset)
        self.assertIsNotNone(train_dataset)
        self.assertIsNotNone(test_dataset)

    def test_tokenize(self):
        tokens = self.processor.tokenize("This is a test sentence.")
        self.assertIsInstance(tokens['input_ids'], list)

if __name__ == '__main__':
    unittest.main()