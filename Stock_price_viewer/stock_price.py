import yfinance as yf
import streamlit as st
import pandas as pd
import json
import requests
from pathlib import Path
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.sidebar.title("Stock Dashboard")


def sidebar():
    stock_name = st.sidebar.text_input("Enter the stock name:", "ORCL", key="stock_name")
    try:
        ticker = yf.Ticker(stock_name)
    except Exception:
        st.warning("Invalid ticker name")
        ticker = None

    period_options = ["1d", "5d", "1mo", "6mo", "1y", "5y"]
    period = st.sidebar.selectbox("Select period", period_options, index=3, key="period")
    interval_options = ["30m", "1h", "1d", "1wk", "1mo"]
    interval = st.sidebar.selectbox("Select interval", interval_options, index=3, key="interval")

    return stock_name, ticker, period, interval

def fetch_history(ticker, period, interval):
    try:
        data = ticker.history(period=period, interval=interval)
        if data is None or data.empty:
            st.warning("No data available for this symbol and time range.")
            return pd.DataFrame()
        return data
    except requests.exceptions.Timeout:
        st.warning("The API took too long to respond.")
        return pd.DataFrame()
    except KeyError as e:
        st.warning(f"Data format changed, missing key: {e}")
        return pd.DataFrame()
    except Exception:
        st.warning("Invalid data for this symbol.")
        return pd.DataFrame()


def chart(data, stock_name, df=None):
    if df is None:
        df = data.reset_index()

    if not data.empty and 'Close' in data.columns:
        data = data.copy()
        data['7-Day SMA'] = data['Close'].rolling(window=7, min_periods=1).mean()
        latest_price = data['Close'].iloc[-1]
        st.metric(label=f"Current price via {stock_name}", value=f"${latest_price:.2f}")
        st.line_chart(data[['Close', '7-Day SMA']])
    else:
        st.metric(label=f"Current price via {stock_name}", value="N/A")
        st.warning("No data available for this symbol.")


def columns(ticker):
    col1, col2, col3, col4 = st.columns(4)
    try:
        info = ticker.info or {}
        with col1:
            previous_close = info.get('previousClose')
            st.metric("Previous Close", f"${previous_close:.2f}" if previous_close is not None else "N/A")
        with col2:
            volume = info.get('volume') or 0
            st.metric("Volume", f"{volume:,}")
        with col3:
            market_cap = info.get('marketCap') or 0
            st.metric("Market Cap", f"${market_cap:,}")
        with col4:
            fifty_two_week_high = info.get('fiftyTwoWeekHigh')
            st.metric("52-Week High", f"${fifty_two_week_high:.2f}" if fifty_two_week_high is not None else "N/A")
    except Exception:
        st.write("Invalid data")


def plotly(stock_name, df):
    with st.expander("Candlestick Chart"):
        if not df.empty and {'Date', 'Open', 'High', 'Low', 'Close'}.issubset(df.columns):
            fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'])])
            fig.update_layout(title=f"{stock_name} Stock Price", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(fig)
        else:
            st.info("Candlestick chart is unavailable for this data range.")
def load_ticker():
    with st.expander("Company and Ticker names (Top 50)"):
        ticker_path = Path(__file__).resolve().parent / "tickers.json"
        with open(ticker_path, 'r', encoding='utf-8') as file:
            ticker_name = json.load(file)
            ticker_name = pd.DataFrame(list(ticker_name.items()), columns=["Ticker", "Company Name"])
            st.dataframe(ticker_name, hide_index=True, use_container_width=True)


def main():
    stock_name, ticker, period, interval = sidebar()

    if ticker is None:
        st.warning("Please enter a valid ticker symbol.")
        return

    data = fetch_history(ticker, period, interval)
    if data.empty:
        return

    df = data.reset_index()
    chart(data, stock_name, df)
    columns(ticker)
    plotly(stock_name, df)
    load_ticker()

if __name__ == "__main__":
    main()






