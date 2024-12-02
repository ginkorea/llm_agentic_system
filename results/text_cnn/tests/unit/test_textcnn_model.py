import unittest
import torch
from workbench.textcnn_project.textcnn_model import TextCNNModel

class TestTextCNNModel(unittest.TestCase):
    def setUp(self):
        self.model = TextCNNModel(embedding_dim=300, kernel_sizes=[3, 4, 5], max_length=50)

    def test_model_initialization(self):
        self.assertEqual(self.model.embedding_dim, 300)
        self.assertEqual(self.model.kernel_sizes, [3, 4, 5])
        self.assertEqual(self.model.max_length, 50)

    def test_forward_pass(self):
        input_data = torch.randint(0, 50, (32, 50))  # batch_size=32, sequence_length=50
        output = self.model(input_data)
        self.assertEqual(output.shape, (32, 1))  # Output should be batch_size x 1

    def test_save_and_load_checkpoint(self):
        self.model.save_checkpoint(epoch=1)
        self.model.load_checkpoint('checkpoint_epoch_1.pth')
        self.assertTrue(True)  # If no exception, test passes

if __name__ == '__main__':
    unittest.main()