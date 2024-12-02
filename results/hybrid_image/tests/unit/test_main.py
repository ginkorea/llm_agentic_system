import unittest
import cv2
import numpy as np
from workbench.hybrid_image_creator.image import Image
from workbench.hybrid_image_creator.hybrid_image_creator import HybridImageCreator

class TestMainFlow(unittest.TestCase):
    def test_main_flow(self):
        image1_data = np.ones((100, 100), dtype=np.uint8) * 255
        image2_data = np.zeros((100, 100), dtype=np.uint8)
        
        image1 = Image(image1_data)
        image2 = Image(image2_data)
        
        hybrid_image = HybridImageCreator.createHybridImage(image1, image2, mixRatio=0.5)
        
        self.assertEqual(hybrid_image.width, 100)
        self.assertEqual(hybrid_image.height, 100)
        self.assertTrue(isinstance(hybrid_image, Image))

if __name__ == '__main__':
    unittest.main()