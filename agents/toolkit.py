from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from langchain_core.tools import tool
from typing import Dict, List
import requests
from const.sk import kc  # Import your API keys from your constants file


class BagOfTools:
    def __init__(self):
        self.tools = []
        self.bind_tools()

    @staticmethod
    @tool
    def calculate(expression: str) -> float:
        """Calculate the result of a mathematical expression."""
        return eval(expression)

    @staticmethod
    @tool
    def to_upper(input_string: str) -> str:
        """Convert a string to uppercase."""
        return input_string.upper()

    @staticmethod
    @tool
    def search(query_parameters: Dict) -> List[Dict]:
        """Perform a web search using Google's JSON API and return top non-visited results as a list of dictionaries."""
        query = query_parameters['query']
        n_sites = query_parameters['n_sites']
        visited_sites = query_parameters.get('visited_sites', [])

        # Prepare the API request URL
        api_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": kc.google_json,  # Google API Key from const.sk
            "cx": kc.google_cx,  # Custom Search Engine ID from const.sk
            "q": query,
            "num": n_sites,  # Number of results to return
        }

        # Make the request to the API
        response = requests.get(api_url, params=params)
        data = response.json()

        # Check if the response contains results
        if "items" not in data:
            return [{"error": "No results found."}]

        # Process the results into a list of dictionaries
        search_results = []
        visited_count = 0

        for item in data["items"]:
            link = item["link"]
            if link not in visited_sites:
                search_result = {
                    "title": item.get("title", "No title"),
                    "link": link,
                    "snippet": item.get("snippet", "No snippet")
                }
                search_results.append(search_result)

                # Mark the site as visited
                visited_sites.append(link)
                visited_count += 1

                if visited_count >= n_sites:
                    break

        return search_results if search_results else [{"error": "No new sites to visit."}]

    @staticmethod
    @tool
    def get_page(url: str) -> str:
        """Visit a URL and return the full text of the page."""
        # Setup headless Chrome options for web scraping
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

        driver = webdriver.Chrome(options=chrome_options)
        try:
            # Visit the page
            driver.get(url)
            time.sleep(3)  # Wait for the page to fully load

            # Get the page source and close the driver
            page_source = driver.page_source
            driver.quit()

            # Parse the content with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            all_the_soup = soup.get_text(separator=' ', strip=True)
            return all_the_soup
        except Exception as e:
            driver.quit()
            return f"Error fetching page content: {str(e)}"

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
