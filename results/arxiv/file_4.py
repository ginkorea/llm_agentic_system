# query_arxiv/paper.py
class Paper:
    def __init__(self, category: str, title: str, author: str, abstract: str, published: str, link: str):
        self.category = category
        self.title = title
        self.author = author
        self.abstract = abstract
        self.published = published
        self.link = link