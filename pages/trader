import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import base64
import json

# -------------------- Initial Settings --------------------
st.set_page_config(page_title="Investment Backtesting Tool", layout="wide")

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {}  # symbol -> {'shares': int, 'cash': float}
if 'cash' not in st.session_state:
    st.session_state.cash = 1000.0  # Initial cash balance
if 'history' not in st.session_state:
    st.session_state.history = []  # List of [date, total_value]

# -------------------- Helper Functions --------------------
def get_stock_price(symbol):
    try:
        data = yf.Ticker(symbol).history(period="1d")
        return data['Close'].iloc[-1]
    except Exception:
        return None

def update_portfolio_value():
    today = datetime.now().strftime("%Y-%m-%d")
    if st.session_state.history and st.session_state.history[-1][0] == today:
        return  # already updated today

    total_value = st.session_state.cash
    for symbol, info in st.session_state.portfolio.items():
        price = get_stock_price(symbol)
        if price:
            total_value += price * info['shares']
    st.session_state.history.append([today, round(total_value, 2)])

def encode_portfolio():
    data = {
        'portfolio': st.session_state.portfolio,
        'cash': st.session_state.cash,
        'history': st.session_state.history
    }
    json_str = json.dumps(data)
    encoded = base64.urlsafe_b64encode(json_str.encode()).decode()
    return f"{st.request.url}?data={encoded}"

def load_from_url():
    query_params = st.query_params
    if "data" in query_params:
        try:
            decoded = base64.urlsafe_b64decode(query_params["data"]).decode()
            data = json.loads(decoded)
            st.session_state.portfolio = data.get('portfolio', {})
            st.session_state.cash = data.get('cash', 1000.0)
            st.session_state.history = data.get('history', [])
            st.success("Portfolio loaded from URL!")
        except Exception as e:
            st.error(f"Failed to load portfolio: {e}")

# -------------------- Main UI --------------------
st.title("📈 Investment Backtesting Tool")
st.markdown("Learn about investing with real data — all pretend!")

load_from_url()

with st.sidebar:
    st.header("📦 Manage Portfolio")
    symbol = st.text_input("Stock symbol (e.g., AAPL)").upper()
    action = st.radio("Action", ["Buy", "Sell"])
    shares = st.number_input("Shares", min_value=1, value=1)

    if st.button(f"{action} Shares"):
        price = get_stock_price(symbol)
        if price is None:
            st.error("Invalid stock symbol or data unavailable.")
        else:
            if action == "Buy":
                total_cost = shares * price
                if st.session_state.cash >= total_cost:
                    if symbol in st.session_state.portfolio:
                        st.session_state.portfolio[symbol]['shares'] += shares
                    else:
                        st.session_state.portfolio[symbol] = {'shares': shares, 'cash': 0.0}
                    st.session_state.cash -= total_cost
                    st.success(f"Bought {shares} shares of {symbol} at ${price:.2f}")
                else:
                    st.warning("Not enough cash to complete the purchase.")
            elif action == "Sell":
                if symbol in st.session_state.portfolio and st.session_state.portfolio[symbol]['shares'] >= shares:
                    st.session_state.portfolio[symbol]['shares'] -= shares
                    proceeds = shares * price
                    st.session_state.cash += proceeds
                    if st.session_state.portfolio[symbol]['shares'] == 0:
                        del st.session_state.portfolio[symbol]
                    st.success(f"Sold {shares} shares of {symbol} at ${price:.2f}")
                else:
                    st.warning("Not enough shares to sell.")

    st.markdown(f"💵 **Cash Balance:** ${st.session_state.cash:.2f}")
    st.markdown("---")
    if st.button("📤 Share Portfolio"):
        link = encode_portfolio()
        st.code(link)

# -------------------- Portfolio Summary --------------------
st.subheader("📊 Portfolio Overview")
if not st.session_state.portfolio:
    st.info("No stocks in your portfolio yet.")
else:
    rows = []
    for symbol, info in st.session_state.portfolio.items():
        price = get_stock_price(symbol)
        value = round(price * info['shares'], 2) if price else 0
        rows.append({
            "Symbol": symbol,
            "Shares": info['shares'],
            "Price": f"${price:.2f}" if price else "N/A",
            "Value": f"${value:.2f}"
        })
    df = pd.DataFrame(rows)
    st.table(df)

# -------------------- Update & Plot --------------------
update_portfolio_value()

st.subheader("📈 Portfolio Value Over Time")
if st.session_state.history:
    df_hist = pd.DataFrame(st.session_state.history, columns=["Date", "Value"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_hist["Date"],
        y=df_hist["Value"],
        mode='lines+markers',
        name="Total Value"
    ))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No portfolio history to display yet.")
