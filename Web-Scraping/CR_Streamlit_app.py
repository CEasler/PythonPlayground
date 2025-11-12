# app.py
import streamlit as st
import pandas as pd
import time
from CryptoRates import CryptoScraper

st.set_page_config(page_title="Crypto Scraper", page_icon="🪙", layout="wide")
st.title("🪙 Crypto Scraper — CentralCharts")

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    pages = st.slider("Pages to scrape", 1, 10, 4)
    do_rescrape = st.button("🔄 Rescrape now")
    st.caption("Use the search box below to find another crypto.")

# Session state
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()
if "last_updated" not in st.session_state:
    st.session_state.last_updated = None

def run_scrape(pages_to_fetch):
    scraper = CryptoScraper(pages_to_fetch)
    with st.spinner("Scraping latest data..."):
        rows, elapsed = scraper.scrape_all()
    if rows:
        df = pd.DataFrame(rows, columns=["Name (Pair)", "Price", "Change", "Open", "High", "Low", "Market Cap"])
        st.session_state.df = df
        st.session_state.last_updated = time.strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"Scraped {len(df)} rows in {elapsed:.2f}s")
    else:
        st.error("No rows found. Try again later.")

# Initial load or rescrape
if st.session_state.df.empty or do_rescrape:
    run_scrape(pages)

# Header info
col1, col2, col3 = st.columns(3)
col1.metric("Rows", len(st.session_state.df))
col2.write(f"**Last Updated:** {st.session_state.last_updated or '—'}")
col3.download_button(
    "Download CSV",
    data=st.session_state.df.to_csv(index=False).encode("utf-8"),
    file_name="crypto_data.csv",
    mime="text/csv"
)

st.divider()

# Search / filter
st.subheader("🔎 Look up a crypto")
query = st.text_input("Enter name or symbol (e.g., bitcoin, btc):", "")
exact = st.checkbox("Exact match", False)

df = st.session_state.df

def filter_df(q, exact):
    if not q:
        return df
    q = q.strip().lower()
    mask = df["Name (Pair)"].str.lower()
    return df[mask.eq(q) if exact else mask.str.contains(q, na=False)]

filtered = filter_df(query, exact)

if not filtered.empty and len(filtered) <= 3 and query:
    st.write("### Result details")
    for _, row in filtered.iterrows():
        with st.container(border=True):
            st.write(f"**{row['Name (Pair)']}**")
            c1, c2, c3 = st.columns(3)
            c1.metric("Price", row["Price"])
            c2.metric("Change", row["Change"])
            c3.metric("Market Cap", row["Market Cap"])
            c4, c5, c6 = st.columns(3)
            c4.write(f"**Open:** {row['Open']}")
            c5.write(f"**High:** {row['High']}")
            c6.write(f"**Low:** {row['Low']}")

st.dataframe(filtered if query else df, use_container_width=True)