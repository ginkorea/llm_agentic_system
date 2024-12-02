from workbench.hybrid_image_creator.image import Image
from workbench.hybrid_image_creator.image_processor import ImageProcessor
from workbench.hybrid_image_creator.hybrid_image_creator import HybridImageCreator

import cv2

def main():
    image1_path = 'path/to/image1.jpg'
    image2_path = 'path/to/image2.jpg'
    
    image1_data = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2_data = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
    
    image1 = Image(image1_data)
    image2 = Image(image2_data)
    
    hybrid_image = HybridImageCreator.createHybridImage(image1, image2, mixRatio=0.5)
    
    cv2.imshow('Hybrid Image', hybrid_image.data)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()