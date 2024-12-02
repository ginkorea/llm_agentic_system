import cv2
import numpy as np
from .image import Image

class ImageProcessor:
    @staticmethod
    def applyGaussianBlur(image: Image, sigma: float, kernelSize: int) -> Image:
        blurred_data = cv2.GaussianBlur(image.data, (kernelSize, kernelSize), sigma)
        return Image(blurred_data)

    @staticmethod
    def applyLowPassFilter(image: Image, cutoff: float) -> Image:
        dft = cv2.dft(np.float32(image.data), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        rows, cols = image.data.shape[:2]
        crow, ccol = rows // 2, cols // 2
        mask = np.zeros((rows, cols, 2), np.uint8)
        mask[crow-int(cutoff):crow+int(cutoff), ccol-int(cutoff):ccol+int(cutoff)] = 1
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = cv2.idft(f_ishift)
        img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])
        return Image(img_back)

    @staticmethod
    def applyHighPassFilter(image: Image, cutoff: float) -> Image:
        dft = cv2.dft(np.float32(image.data), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        rows, cols = image.data.shape[:2]
        crow, ccol = rows // 2, cols // 2
        mask = np.ones((rows, cols, 2), np.uint8)
        mask[crow-int(cutoff):crow+int(cutoff), ccol-int(cutoff):ccol+int(cutoff)] = 0
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = cv2.idft(f_ishift)
        img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])
        return Image(img_back)

    @staticmethod
    def performConvolution(image: Image, kernel: np.ndarray) -> Image:
        convolved_data = cv2.filter2D(image.data, -1, kernel)
        return Image(convolved_data)

    @staticmethod
    def performCrossCorrelation(image: Image, template: Image) -> Image:
        result = cv2.matchTemplate(image.data, template.data, cv2.TM_CCORR)
        return Image(result)