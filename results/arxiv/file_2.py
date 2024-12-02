# query_arxiv/query_arxiv.py
from workbench.query_arxiv.query_params import QueryParams
from workbench.query_arxiv.arxiv_api import ArXivAPI
from workbench.query_arxiv.xml_parser import XMLParser
from workbench.query_arxiv.date_filter import DateFilter

class QueryArXiv:
    def executeQuery(self, params: QueryParams):
        api = ArXivAPI()
        xml_data = api.fetchData(params)
        parser = XMLParser()
        papers = parser.parse(xml_data)
        filter = DateFilter()
        return filter.filterByRecentDays(papers, params.recent_days)

    def printResults(self, papers, verbose: bool):
        if verbose:
            for paper in papers:
                print(f"Title: {paper.title}, Author: {paper.author}, Published: {paper.published}")

    def saveResultsToCSV(self, papers, filePath: str):
        import csv
        with open(filePath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Category', 'Title', 'Author', 'Abstract', 'Published', 'Link'])
            for paper in papers:
                writer.writerow([paper.category, paper.title, paper.author, paper.abstract, paper.published, paper.link])