import unittest
from unittest.mock import patch
from workbench.chakin.progress_bar import ProgressBar

class TestProgressBar(unittest.TestCase):
    @patch('builtins.print')
    def test_start(self, mock_print):
        bar = ProgressBar()
        bar.start()
        mock_print.assert_called_with("Starting download...")

    @patch('builtins.print')
    def test_update(self, mock_print):
        bar = ProgressBar()
        bar.update(0.5)
        mock_print.assert_called_with("Download progress: 50.00%")

    @patch('builtins.print')
    def test_finish(self, mock_print):
        bar = ProgressBar()
        bar.finish()
        mock_print.assert_called_with("Download finished.")

if __name__ == '__main__':
    unittest.main()