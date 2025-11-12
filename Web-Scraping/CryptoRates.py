# scraper.py
import time
import requests
from bs4 import BeautifulSoup as bs

class CryptoScraper:
    BASE_URL = "https://www.centralcharts.com/en/price-list-ranking/ALL/desc/ts_82-cryptocurrencies-usd--qc_13-capitalization?p={}"
    HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CryptoRatesBot/1.0)"}

    def __init__(self, pages=4):
        self.pages_to_scrape = pages
        self.values_list = []

    def fetch_page(self, page_number):
        url = self.BASE_URL.format(page_number)
        try:
            resp = requests.get(url, headers=self.HEADERS, timeout=15)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException:
            return None

    def parse_page(self, html_text):
        soup = bs(html_text, 'html.parser')
        table = soup.find('table', class_='tabMini tabQuotes') or soup.select_one('table.tabMini.tabQuotes')
        if not table:
            return []
        rows = []
        for tr in table.find_all('tr')[1:]:
            tds = tr.find_all('td')
            if not tds:
                continue
            rows.append([td.get_text(strip=True) for td in tds[:7]])
        return rows

    def scrape_all(self):
        """Returns (rows_list, elapsed_seconds) — ALWAYS exactly two values."""
        start = time.time()
        all_rows = []
        for p in range(1, self.pages_to_scrape + 1):
            html = self.fetch_page(p)
            if html:
                all_rows.extend(self.parse_page(html))
        self.values_list = all_rows  # list only, not a tuple
        elapsed = time.time() - start
        return all_rows, elapsed  # exactly two values