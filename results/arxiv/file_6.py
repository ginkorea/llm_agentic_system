# query_arxiv/xml_parser.py
import xmltodict
from workbench.query_arxiv.paper import Paper

class XMLParser:
    def parse(self, xmlData):
        data = xmltodict.parse(xmlData)
        papers = []
        for entry in data['feed']['entry']:
            paper = Paper(
                category=entry['category']['@term'],
                title=entry['title'],
                author=entry['author']['name'],
                abstract=entry['summary'],
                published=entry['published'],
                link=entry['id']
            )
            papers.append(paper)
        return papers