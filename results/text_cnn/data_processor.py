from datasets import load_dataset
from transformers import BertTokenizer

class DataProcessor:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def load_dataset(self):
        dataset = load_dataset('imdb')
        return dataset

    def preprocess_data(self, dataset):
        # Preprocess and tokenize dataset
        tokenized_data = dataset.map(lambda x: self.tokenizer(x['text'], padding='max_length', truncation=True))
        train_dataset = tokenized_data['train'].train_test_split(test_size=0.1)
        return train_dataset['train'], train_dataset['test']

    def tokenize(self, text):
        return self.tokenizer(text, padding='max_length', truncation=True)