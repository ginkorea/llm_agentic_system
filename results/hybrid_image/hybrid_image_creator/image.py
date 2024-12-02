import numpy as np

class Image:
    def __init__(self, data: np.ndarray):
        self.data = data
        self.height, self.width = data.shape[:2]