# app.py (snippet)
import streamlit as st
import pandas as pd
import time
from CryptoRates import CryptoScraper

def run_scrape(pages_to_fetch: int):
    scraper = CryptoScraper(pages_to_fetch)
    with st.spinner("Scraping latest data..."):
        result = scraper.scrape_all()

    # Defensive unpacking: accept (rows, elapsed) or just [rows]
    rows, elapsed = None, None
    if isinstance(result, tuple):
        if len(result) >= 2:
            rows, elapsed = result[0], result[1]
        elif len(result) == 1:
            rows = result[0]
    else:
        rows = result

    if rows:
        df = pd.DataFrame(rows, columns=[
            "Name (Pair)", "Price", "Change", "Open", "High", "Low", "Market Cap"
        ])
        st.session_state.df = df
        st.session_state.last_updated = time.strftime("%Y-%m-%d %H:%M:%S")
        if elapsed is not None:
            st.success(f"Scraped {len(df)} rows in {elapsed:.2f}s")
        else:
            st.success(f"Scraped {len(df)} rows.")
    else:
        st.error("No rows were scraped. Try again or reduce the number of pages.")