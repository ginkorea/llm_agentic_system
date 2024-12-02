from .image_processor import ImageProcessor
from .image import Image

class HybridImageCreator:
    @staticmethod
    def createHybridImage(image1: Image, image2: Image, mixRatio: float) -> Image:
        low_pass = ImageProcessor.applyLowPassFilter(image1, cutoff=30)
        high_pass = ImageProcessor.applyHighPassFilter(image2, cutoff=30)
        hybrid_data = cv2.addWeighted(low_pass.data, mixRatio, high_pass.data, 1 - mixRatio, 0)
        return Image(hybrid_data)