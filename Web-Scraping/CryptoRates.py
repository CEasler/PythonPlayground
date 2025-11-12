from bs4 import BeautifulSoup as bs
import requests
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CryptoRatesBot/1.0)"}

start_time = time.time()

pages = []
for page_number in range(1, 5):
    url = f'https://www.centralcharts.com/en/price-list-ranking/ALL/desc/ts_82-cryptocurrencies-usd--qc_13-capitalization?p={page_number}'
    pages.append(url)

values_list = []
for page in pages:
    try:
        resp = requests.get(page, headers=HEADERS, timeout=15)
    except requests.RequestException as e:
        print(f"[error] request failed for {page}: {e}")
        continue

    if resp.status_code != 200 or not resp.text:
        print(f"[warn] bad response for {page}: status={resp.status_code}, len={len(resp.text) if resp.text else 0}")
        continue

    soup = bs(resp.text, 'html.parser')

    # Try both class-based and CSS selector (more robust if class order/spacing changes)
    stock_table = soup.find('table', class_='tabMini tabQuotes')
    if not stock_table:
        stock_table = soup.select_one('table.tabMini.tabQuotes')


    tr_tag_list = stock_table.find_all('tr')

    for each_tr_tag in tr_tag_list[1:]:
        td_tag_list = each_tr_tag.find_all('td')
        if not td_tag_list:
            continue
        row_values = [td.get_text(strip=True) for td in td_tag_list[:7]]
        values_list.append(row_values)

# After scraping and building values_list
# Example: values_list = [['BITCOIN - BTC/USD', '106,196.26', ...], ...]
# Ask user which crypto they want to prompt for data
user_crypto = input("Enter the crypto name or symbol (e.g. 'bitcoin' or 'btc'): ").strip().lower()

found = False
for row in values_list:
    name = row[0].lower()
    if user_crypto in name:
        print(f"\nData for {row[0]}:")
        print(f"Current Price: {row[1]}")
        print(f"Change: {row[2]}")
        print(f"Open: {row[3]}")
        print(f"High: {row[4]}")
        print(f"Low: {row[5]}")
        print(f"Market Cap: {row[6]}")
        found = True
        break

if not found:
    print("Crypto not found. Try another name or symbol.")

print('--- code finished in %.3f seconds ---' % (time.time() - start_time))


#I decided to use streamlit to create a small model website to display our data
"""import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Simple Crypto Rate App", layout="centered")
st.write("Hello World")"""