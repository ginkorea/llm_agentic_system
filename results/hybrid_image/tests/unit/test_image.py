import unittest
import numpy as np
from workbench.hybrid_image_creator.image import Image

class TestImage(unittest.TestCase):
    def test_image_initialization(self):
        data = np.zeros((100, 100), dtype=np.uint8)
        image = Image(data)
        self.assertEqual(image.width, 100)
        self.assertEqual(image.height, 100)
        self.assertTrue((image.data == data).all())

    def test_image_dimensions(self):
        data = np.random.randint(0, 256, size=(150, 200), dtype=np.uint8)
        image = Image(data)
        self.assertEqual(image.width, 200)
        self.assertEqual(image.height, 150)

if __name__ == '__main__':
    unittest.main()