class ProgressBar:
    def start(self):
        print("Starting download...")

    def update(self, progress: float):
        print(f"Download progress: {progress * 100:.2f}%")

    def finish(self):
        print("Download finished.")