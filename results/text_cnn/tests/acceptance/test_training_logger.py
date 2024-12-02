import unittest
from workbench.textcnn_project.training_logger import TrainingLogger

class TestTrainingLogger(unittest.TestCase):
    def setUp(self):
        self.logger = TrainingLogger()

    def test_log_training_loss(self):
        self.logger.log_training_loss(batch=1, loss=0.5)
        self.assertIn("Batch 1: Loss 0.5", self.logger.logs)

    def test_log_accuracy(self):
        self.logger.log_accuracy(epoch=1, accuracy=0.8)
        self.assertIn("Epoch 1: Accuracy 0.8", self.logger.logs)

if __name__ == '__main__':
    unittest.main()