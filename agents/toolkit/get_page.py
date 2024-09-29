from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from langchain_core.tools import tool


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