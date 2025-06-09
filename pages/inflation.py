import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# Page configurations
st.set_page_config(
    page_title="Future Value Calculator",
    page_icon="📈",
    layout="centered"
)

# Fun explanation for kids
st.markdown("""
<div style="background-color:#e8f5e9; padding:20px; border-radius:12px; margin-bottom:25px; border-left: 5px solid #2e7d32; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <h2 style="color:#1b5e20; margin-top:0; border-bottom: 2px dashed #81c784; padding-bottom:10px;">
        🎈 What is Inflation? 🎈
    </h2>
    <p style="color:#2e7d32; font-size:1.1em;">
        Imagine you have a magic money box. Today, you can buy 10 lollipops with your money. But guess what? Next year, the same money might only buy 9 lollipops! 🍭
    </p>
    <p style="color:#2e7d32; font-size:1.1em;">
        That's <span style="color:#d32f2f; font-weight:bold; background-color:#ffebee; padding:2px 6px; border-radius:4px;">inflation</span> - when things get more expensive over time. It's like your money is a balloon that slowly loses air! 🎈💨
    </p>
    <div style="background-color:#e8f5e9; border:2px dashed #4caf50; border-radius:8px; padding:12px; margin-top:15px;">
        <p style="color:#1b5e20; margin:0; font-weight:bold; text-align:center;">
            But don't worry! This tool will show you how to make your money grow faster than prices go up! 💰✨
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
<style>
    .item-option {
        border: 2px solid #a5d6a7;
        border-radius: 12px;
        padding: 15px;
        margin: 12px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        background-color: #f1f8e9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .item-option:hover {
        border-color: #43a047;
        background-color: #e8f5e9;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(67, 160, 71, 0.2);
    }
    .item-option.selected {
        border-color: #4CAF50;
        background-color: #f0f8f0;
    }
    .result-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .stSlider > div > div > div {
        background-color: #4CAF50 !important;
    }
    .stSelectbox > div > div > div {
        border-color: #4CAF50 !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("💰 Future Value Calculator")
st.markdown("### See how inflation affects your purchasing power")

# Item selection with fixed prices
ITEMS = {
    "pizza": {"emoji": "🍕", "name": "Pizza", "price": 10.00},
    "game": {"emoji": "🎮", "name": "Video Game", "price": 60.00},
    "disney": {"emoji": "🏰", "name": "Disney+ Subscription", "price": 20.00}
}

# Display item options
st.subheader("1. Choose an item")
selected_item = st.radio(
    "Select an item:",
    options=list(ITEMS.keys()),
    format_func=lambda x: f"{ITEMS[x]['emoji']} {ITEMS[x]['name']} (${ITEMS[x]['price']:.2f})",
    label_visibility="collapsed"
)

# Get the selected item's details
item = ITEMS[selected_item]

# Investment amount selection
st.subheader("2. How much money do you have?")
amount = st.selectbox(
    "Select an amount:",
    options=[100, 200, 500, 750, 1000, 10000, 50000],
    format_func=lambda x: f"${x:,}"
)

# Stock market indices with their tickers and average returns
STOCK_INDICES = {
    "S&P 500 (SPY)": "SPY",
    "NASDAQ-100 (QQQ)": "QQQ",
    "Dow Jones (DIA)": "DIA",
    "MSCI World (URTH)": "URTH",
    "S&P 500 Growth (IVW)": "IVW"
}

# Default values
DEFAULT_INFLATION = 3.0  # 3% annual inflation
DEFAULT_YEARS = 5
DEFAULT_AMOUNT = 1000

# Function to get historical performance of an index
def get_index_performance(ticker, years=5):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*years)
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if not df.empty and len(df) > 1:  # Ensure we have enough data points
            start_price = float(df['Close'].iloc[0])
            end_price = float(df['Close'].iloc[-1])
            if start_price > 0:  # Avoid division by zero
                return float(((end_price / start_price) ** (1/years) - 1) * 100)
    except Exception as e:
        print(f"Error getting performance for {ticker}: {e}")
    return 7.0  # Default return if data fetch fails

# Time horizon
st.subheader("3. Time period")
years = st.slider("How many years into the future?", 1, 30, 5, 1)

# Calculate results
def calculate_items(amount, price, years, inflation_rate):
    items_now = amount / price
    future_price = price * ((1 + (inflation_rate/100)) ** years)
    items_future = amount / future_price
    return {
        "items_now": items_now,
        "items_future": items_future,
        "future_price": future_price,
        "items_lost": items_now - items_future
    }

# Calculate
results = calculate_items(amount, item["price"], years, DEFAULT_INFLATION)
# Ensure all required keys are in the results dictionary
results.update({
    'item_name': item['name'],
    'item_price': item['price']
})

# Display results
st.markdown("---")
st.subheader("📊 Results")

# Current purchasing power
st.markdown(f"""
<div class='result-box'>
    <h3>Today with ${amount:,.2f} you can buy:</h3>
    <div style='font-size: 2.5rem; color: #4CAF50; font-weight: bold; margin: 10px 0;'>
        {results['items_now']:,.1f} {item['name']}s
    </div>
    <p>At ${item['price']:,.2f} each</p>
</div>
""", unsafe_allow_html=True)

# Future purchasing power
st.markdown(f"""
<div class='result-box'>
    <h3>In {years} years with ${amount:,.2f} you could buy:</h3>
    <div style='font-size: 2.5rem; color: #e74c3c; font-weight: bold; margin: 10px 0;'>
        {results['items_future']:,.1f} {item['name']}s
    </div>
    <p>At ${results['future_price']:,.2f} each ({DEFAULT_INFLATION}% annual inflation)</p>
</div>
""", unsafe_allow_html=True)

# Comparison
col1, col2, col3 = st.columns([1, 0.2, 1])

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 20px; border-radius: 10px; background-color: #f8f9fa;'>
        <div style='font-size: 2.5rem; font-weight: bold;'>{:,.0f}</div>
        <div style='font-size: 1.2rem;'>{}s Today</div>
        <div style='color: #666;'>${:.2f} each</div>
    </div>
    """.format(round(results['items_now']), results['item_name'], item['price']), unsafe_allow_html=True)

with col2:
    st.markdown("<div style='height: 100%; display: flex; align-items: center; justify-content: center;'><span style='font-size: 2.5rem;'>→</span></div>", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align: center; padding: 20px; border-radius: 10px; background-color: #f8f9fa;'>
        <div style='font-size: 2.5rem; font-weight: bold;'>{:,.0f}</div>
        <div style='font-size: 1.2rem;'>{}s in {} years</div>
        <div style='color: #666;'>${:.2f} each</div>
    </div>
    """.format(round(results['items_future']), results['item_name'], years, results['future_price']), unsafe_allow_html=True)

st.markdown(f"""
<div style='text-align: center; margin: 20px 0; padding: 15px; background-color: #fff8f8; border-radius: 10px;'>
    <p style='color: #e74c3c; font-weight: bold; margin: 0;'>
        You'll be able to buy {round(results['items_lost'])} fewer {results['item_name']}s with the same amount of money!
    </p>
</div>
""", unsafe_allow_html=True)

# Investment comparison
st.markdown("---")
st.markdown("""
<div style="background-color:#e8f5e9; padding:15px; border-radius:10px; margin:20px 0; border-left: 5px solid #2e7d32;">
    <h2 style="color:#1b5e20; margin:0 0 10px 0;">📈 Investment Options</h2>
    <p style="color:#2e7d32; margin:0;">Compare how your money could grow if invested in different market indices:</p>
</div>
""", unsafe_allow_html=True)

# Calculate performance for each index
index_performance = {}
for name, ticker in STOCK_INDICES.items():
    return_rate = get_index_performance(ticker, years=5)
    # Ensure we have a numeric value
    index_performance[name] = float(return_rate) if return_rate is not None else 7.0

# Sort by performance (convert to list of tuples first)
sorted_indices = sorted([(k, v) for k, v in index_performance.items()], 
                       key=lambda x: x[1], 
                       reverse=True)

# Store the indices with their return rates
index_options = []
index_returns = {}

for name, return_rate in sorted_indices:
    display_text = f"{name} ({return_rate:.1f}% annual return)"
    index_options.append(display_text)
    index_returns[display_text] = return_rate

# Display index selection
selected_index = st.selectbox(
    "Choose a market index:",
    index_options,
    index=0
)

# Get the selected return rate
selected_return = index_returns[selected_index]

# Calculate investment growth
investment_value = amount * ((1 + (selected_return/100)) ** years)
items_with_investment = investment_value / results['future_price']

# Display investment comparison
st.markdown("""
<div style='margin: 30px 0; padding: 20px; border-radius: 12px; background-color: #f1f8e9; border: 2px solid #a5d6a7; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
    <h3 style='margin: 0 0 15px 0; color: #1b5e20; border-bottom: 2px dashed #81c784; padding-bottom: 10px;'>💰 Investment Potential</h3>
    <div style='display: flex; justify-content: space-between; margin: 15px 0;'>
        <div style='text-align: center; flex: 1; background: #e8f5e9; padding: 15px; border-radius: 8px; margin: 5px;'>
            <div style='font-size: 1.2rem; color: #2e7d32;'>Initial Investment</div>
            <div style='font-size: 2rem; font-weight: bold; color: #1b5e20;'>${:,.0f}</div>
        </div>
        <div style='display: flex; align-items: center; padding: 0 10px;'>
            <span style='font-size: 2rem; color: #2e7d32;'>→</span>
        </div>
        <div style='text-align: center; flex: 1; background: #e8f5e9; padding: 15px; border-radius: 8px; margin: 5px;'>
            <div style='font-size: 1.2rem; color: #2e7d32;'>Potential Value in {} Years</div>
            <div style='font-size: 2rem; font-weight: bold; color: #1b5e20;'>${:,.0f}</div>
        </div>
    </div>
    <div style='text-align: center; margin: 20px 0; padding: 15px; background-color: #e8f5e9; border: 2px dashed #81c784; border-radius: 8px;'>
        <p style='margin: 5px 0; font-size: 1.1rem; color: #2e7d32;'>With this investment, you could buy:</p>
        <p style='margin: 10px 0; font-size: 1.8rem; font-weight: bold; color: #1b5e20;'>{:,.0f} {}s</p>
        <p style='margin: 5px 0; font-size: 1em; color: #2e7d32; background: #f1f8e9; padding: 8px; border-radius: 6px;'>
            🆚 Compared to <span style='font-weight:bold;'>{:,.0f}</span> if you spent the money now
        </p>
    </div>
    <p style='font-size: 0.9em; color: #2e7d32; margin: 20px 0 0 0; text-align: center; padding: 10px; background: #e8f5e9; border-radius: 6px;'>
        📊 Based on <span style='font-weight:bold;'>{}%</span> average annual return. Past performance is not indicative of future results.
    </p>
</div>
""".format(
    amount, years, round(investment_value, 2), 
    int(round(items_with_investment)), results['item_name'],
    int(round(results['items_now'])),
    round(selected_return, 1)
), unsafe_allow_html=True)