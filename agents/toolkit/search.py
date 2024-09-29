from typing import Dict, List
from langchain_core.tools import tool
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from const.sk import kc


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


