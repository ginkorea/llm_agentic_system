from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from langchain_core.tools import tool
from typing import Dict, List
import requests
from const.sk import kc  # Import your API keys from your constants file
from agents.toolkit.search import search
from agents.toolkit.get_page import get_page
from agents.toolkit.calculate import calculate
from agents.toolkit.to_upper import to_upper


class BagOfTools:
    def __init__(self):
        self.tools = []
        self.bind_tools()
        self.search = search
        self.get_page = get_page
        self.calculate = calculate
        self.to_upper = to_upper


    def bind_tools(self):
        """Method to bind all tool methods inside the BagOfTools."""
        for name, method in self.__class__.__dict__.items():
            if callable(method) and hasattr(getattr(self, name), "as_tool"):
                structured_tool = getattr(self, name).as_tool()
                desc = structured_tool.description.split(".")[0]  # Get the first sentence of the description
                self.tools.append({"name": name, "desc": desc, "tool": getattr(self, name)})

    def get_tools(self, verbose: bool = True):
        """Returns the list of all tools."""
        if verbose:
            print("Available tools:")
        for _tool in self.tools:
            if verbose:
                print(f"--{_tool['name']}: {_tool['desc'][23:]}")
        return self.tools


# Example usage
if __name__ == "__main__":
    bot = BagOfTools()
    tools = bot.get_tools()
    search_q = {"query_parameters": {"query": "how do you multiply matrices in your head", "n_sites": 3,
                                     "visited_sites": ["https://www.python.org/"]}}

    results = bot.search(search_q)
    for result in results:
        print(result)
        full_text = bot.get_page(result["link"])
        print(full_text)
