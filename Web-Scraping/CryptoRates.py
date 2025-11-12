from bs4 import BeautifulSoup as bs
import requests
import time


class CryptoScraper:
    BASE_URL = "https://www.centralcharts.com/en/price-list-ranking/ALL/desc/ts_82-cryptocurrencies-usd--qc_13-capitalization?p={}"
    HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CryptoRatesBot/1.0)"}
    page_number = 4
    def __init__(self, pages=4):
        self.pages_to_scrape = pages
        self.values_list = []

    def fetch_page(self, page_number):
        """Fetch and return the HTML content for a given page number."""
        url = self.BASE_URL.format(page_number)
        try:
            resp = requests.get(url, headers=self.HEADERS, timeout=15)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            print(f"[error] Request failed for page {page_number}: {e}")
            return None

    def parse_page(self, html_text):
        """Parse the HTML and extract crypto data rows."""
        soup = bs(html_text, 'html.parser')
        stock_table = soup.find('table', class_='tabMini tabQuotes') or soup.select_one('table.tabMini.tabQuotes')
        if not stock_table:
            print("[warn] Could not find table on page.")
            return []

        rows = []
        for tr in stock_table.find_all('tr')[1:]:
            td_list = tr.find_all('td')
            if not td_list:
                continue
            row_values = [td.get_text(strip=True) for td in td_list[:7]]
            rows.append(row_values)
        return rows

    def scrape_all(self):
        """Scrape all pages and build a full dataset."""
        start_time = time.time()
        for page_num in range(1, self.pages_to_scrape + 1):
            html = self.fetch_page(page_num)
            if html:
                page_data = self.parse_page(html)
                self.values_list.extend(page_data)
        print(f"--- Scraping finished in {time.time() - start_time:.3f} seconds ---")
        return self.values_list

    def find_crypto(self, query):
        """Search for a cryptocurrency by name or symbol."""
        query = query.strip().lower()
        for row in self.values_list:
            name = row[0].lower()
            if query in name:
                print(f"\nData for {row[0]}:")
                print(f"Current Price: {row[1]}")
                print(f"Change: {row[2]}")
                print(f"Open: {row[3]}")
                print(f"High: {row[4]}")
                print(f"Low: {row[5]}")
                print(f"Market Cap: {row[6]}")
                return row
        print("Crypto not found. Try another name or symbol.")
        return None


if __name__ == "__main__":
    scraper = CryptoScraper(pages=4)
    scraper.scrape_all()
    user_input = input("Enter the crypto name or symbol (e.g. 'bitcoin' or 'btc'): ")
    scraper.find_crypto(user_input)
