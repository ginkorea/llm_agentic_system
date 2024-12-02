import unittest
import numpy as np
import cv2
from workbench.hybrid_image_creator.image import Image
from workbench.hybrid_image_creator.image_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.data = np.ones((100, 100), dtype=np.uint8) * 255
        self.image = Image(self.data)

    def test_apply_gaussian_blur(self):
        blurred_image = ImageProcessor.applyGaussianBlur(self.image, sigma=1.0, kernelSize=5)
        self.assertEqual(blurred_image.width, self.image.width)
        self.assertEqual(blurred_image.height, self.image.height)

    def test_apply_low_pass_filter(self):
        low_pass_image = ImageProcessor.applyLowPassFilter(self.image, cutoff=30)
        self.assertEqual(low_pass_image.width, self.image.width)
        self.assertEqual(low_pass_image.height, self.image.height)

    def test_apply_high_pass_filter(self):
        high_pass_image = ImageProcessor.applyHighPassFilter(self.image, cutoff=30)
        self.assertEqual(high_pass_image.width, self.image.width)
        self.assertEqual(high_pass_image.height, self.image.height)

    def test_perform_convolution(self):
        kernel = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
        convolved_image = ImageProcessor.performConvolution(self.image, kernel)
        self.assertEqual(convolved_image.width, self.image.width)
        self.assertEqual(convolved_image.height, self.image.height)

    def test_perform_cross_correlation(self):
        template = Image(np.ones((10, 10), dtype=np.uint8) * 255)
        result = ImageProcessor.performCrossCorrelation(self.image, template)
        self.assertIsInstance(result, Image)

if __name__ == '__main__':
    unittest.main()