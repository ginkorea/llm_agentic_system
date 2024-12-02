# query_arxiv/arxiv_api.py
import requests

class ArXivAPI:
    def fetchData(self, params):
        query = f"http://export.arxiv.org/api/query?search_query=cat:{params.category}+AND+au:{params.author}+AND+ti:{params.title}+AND+abs:{params.abstract}&sortBy=submittedDate&sortOrder=descending&start=0&max_results={params.max_results}"
        response = requests.get(query)
        return response.content