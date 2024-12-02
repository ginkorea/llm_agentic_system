import unittest
import numpy as np
from workbench.hybrid_image_creator.image import Image
from workbench.hybrid_image_creator.hybrid_image_creator import HybridImageCreator

class TestHybridImageCreator(unittest.TestCase):
    def setUp(self):
        self.data1 = np.ones((100, 100), dtype=np.uint8) * 255
        self.data2 = np.zeros((100, 100), dtype=np.uint8)
        self.image1 = Image(self.data1)
        self.image2 = Image(self.data2)

    def test_create_hybrid_image(self):
        hybrid_image = HybridImageCreator.createHybridImage(self.image1, self.image2, mixRatio=0.5)
        self.assertEqual(hybrid_image.width, self.image1.width)
        self.assertEqual(hybrid_image.height, self.image1.height)
        self.assertTrue(isinstance(hybrid_image, Image))

    def test_hybrid_image_content(self):
        hybrid_image = HybridImageCreator.createHybridImage(self.image1, self.image2, mixRatio=0.5)
        self.assertTrue(np.any(hybrid_image.data != self.image1.data))
        self.assertTrue(np.any(hybrid_image.data != self.image2.data))

if __name__ == '__main__':
    unittest.main()