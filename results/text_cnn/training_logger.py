class TrainingLogger:
    def __init__(self):
        self.logs = []

    def log_training_loss(self, batch, loss):
        log_entry = f"Batch {batch}: Loss {loss}"
        print(log_entry)
        self.logs.append(log_entry)

    def log_accuracy(self, epoch, accuracy):
        log_entry = f"Epoch {epoch}: Accuracy {accuracy}"
        print(log_entry)
        self.logs.append(log_entry)