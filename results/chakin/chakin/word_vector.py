class WordVector:
    def __init__(self, name: str, dimension: int, corpus: str, vocabulary_size: int, method: str, language: str, paper: str, author: str, url: str):
        self.name = name
        self.dimension = dimension
        self.corpus = corpus
        self.vocabulary_size = vocabulary_size
        self.method = method
        self.language = language
        self.paper = paper
        self.author = author
        self.url = url