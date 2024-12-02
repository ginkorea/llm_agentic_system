import numpy as np

class ModelEvaluator:
    def calculate_accuracy(self, predictions, labels):
        predictions = np.round(predictions)
        accuracy = np.mean(predictions == labels)
        return accuracy