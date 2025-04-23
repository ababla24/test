import streamlit as st
import yfinance as yf
import pandas as pd

# Simulated user database (for demo only)
user_watchlists = {
    "john@example.com": ["AAPL", "TSLA"],
    "jane@example.com": ["GOOGL", "AMZN"]
}

# --- Sidebar ---
st.sidebar.title("AztecInvest 💸")
email = st.sidebar.text_input("Enter your email to log in")

if email:
    if email not in user_watchlists:
        user_watchlists[email] = []
    st.sidebar.success(f"Logged in as {email}")

    # Add to watchlist
    new_ticker = st.sidebar.text_input("Add a stock to your watchlist")
    if st.sidebar.button("Add") and new_ticker:
        user_watchlists[email].append(new_ticker.upper())
        st.sidebar.success(f"Added {new_ticker.upper()} to your watchlist")

    # Show watchlist
    st.sidebar.write("**Your Watchlist:**")
    st.sidebar.write(user_watchlists[email])

# --- Main ---
st.title("Welcome to AztecInvest 📈")

st.header("Top Stocks Among SDSU Students")
all_stocks = sum(user_watchlists.values(), [])
top_stocks = pd.Series(all_stocks).value_counts().head(5)
st.table(top_stocks)

# --- Stock Data Viewer ---
st.header("Stock Data Viewer")
ticker_input = st.text_input("Enter a stock ticker to view historical data")

if ticker_input:
    try:
        stock = yf.Ticker(ticker_input.upper())
        hist = stock.history(period="1y")
        st.subheader(stock.info.get('longName', ticker_input.upper()))
        st.line_chart(hist['Close'])
        st.write(hist.tail())
    except Exception as e:
        st.error("Error fetching data. Please check the ticker symbol.")

# --- Stock Comparison Tool ---
st.header("Stock Comparison Tool")
col1, col2 = st.columns(2)

with col1:
    ticker1 = st.text_input("First Ticker")
with col2:
    ticker2 = st.text_input("Second Ticker")

if ticker1 and ticker2:
    try:
        s1 = yf.Ticker(ticker1.upper())
        s2 = yf.Ticker(ticker2.upper())

        name1 = s1.info.get('shortName', ticker1.upper())
        name2 = s2.info.get('shortName', ticker2.upper())

        price1 = s1.info.get('regularMarketPrice', 0)
        price2 = s2.info.get('regularMarketPrice', 0)

        st.write(f"**{name1}**: ${price1:.2f}")
        st.write(f"**{name2}**: ${price2:.2f}")

        hist1 = s1.history(period="1y")['Close']
        hist2 = s2.history(period="1y")['Close']

        df_compare = pd.DataFrame({ticker1.upper(): hist1, ticker2.upper(): hist2})
        st.line_chart(df_compare)
    except Exception as e:
        st.error("Error comparing stocks. Please check the ticker symbols.")
