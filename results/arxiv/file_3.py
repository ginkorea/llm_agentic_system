# query_arxiv/query_params.py
class QueryParams:
    def __init__(self, category: str = "", title: str = "", author: str = "", abstract: str = "", recent_days: int = 0, max_results: int = 10):
        self.category = category
        self.title = title
        self.author = author
        self.abstract = abstract
        self.recent_days = recent_days
        self.max_results = max_results