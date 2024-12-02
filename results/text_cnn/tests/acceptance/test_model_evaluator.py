import unittest
import numpy as np
from workbench.textcnn_project.model_evaluator import ModelEvaluator

class TestModelEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = ModelEvaluator()

    def test_calculate_accuracy(self):
        predictions = np.array([0, 1, 1, 0])
        labels = np.array([0, 1, 0, 0])
        accuracy = self.evaluator.calculate_accuracy(predictions, labels)
        self.assertEqual(accuracy, 0.75)

if __name__ == '__main__':
    unittest.main()