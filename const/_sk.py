import os

# Define the API keys and tokens
# Replace the placeholders with your own keys
# remove the underscore from the file name
# e.g. _sk.py -> sk.py

class KeyChain:

    def __init__(self):
        self.open_ai = "your_key"
        self.google_json = "your_json"
        self.google_cx = "your_cx"
kc = KeyChain()

os.environ["OPENAI_API_KEY"] = kc.open_ai