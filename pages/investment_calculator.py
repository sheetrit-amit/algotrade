import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Investment Backtesting Tool 📊",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .profit-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    .loss-box {
        background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    .info-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .sidebar .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 Investment Backtesting Tool</h1>
    <p>Discover how much you could have made with past investments!</p>
    <p><em>Powered by real market data</em></p>
</div>
""", unsafe_allow_html=True)

# Expanded stock selection with categories
STOCK_CATEGORIES = {
    'Tech Giants': {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Google (Alphabet)': 'GOOGL',
        'Amazon': 'AMZN',
        'Meta (Facebook)': 'META',
        'Netflix': 'NFLX',
        'Adobe': 'ADBE',
        'Salesforce': 'CRM',
        'NVIDIA': 'NVDA',
        'Intel': 'INTC'
    },
    'Consumer Brands': {
        'Tesla': 'TSLA',
        'Disney': 'DIS',
        'McDonald\'s': 'MCD',
        'Nike': 'NKE',
        'Coca-Cola': 'KO',
        'Starbucks': 'SBUX',
        'Home Depot': 'HD',
        'Walmart': 'WMT',
        'Procter & Gamble': 'PG',
        'Johnson & Johnson': 'JNJ'
    },
    'Financial': {
        'Berkshire Hathaway': 'BRK-B',
        'JPMorgan Chase': 'JPM',
        'Bank of America': 'BAC',
        'Wells Fargo': 'WFC',
        'Goldman Sachs': 'GS',
        'American Express': 'AXP',
        'PayPal': 'PYPL',
        'Visa': 'V',
        'Mastercard': 'MA'
    },
    'Crypto ETFs': {
        'Bitcoin ETF (BITO)': 'BITO',
        'Ethereum ETF (ETHE)': 'ETHE'
    }
}

# Sidebar configuration
with st.sidebar:
    st.header("🎯 Configure Your Investment")
    
    # Category selection
    category = st.selectbox("Select Category:", list(STOCK_CATEGORIES.keys()))
    
    # Stock selection within category
    selected_company = st.selectbox("Choose Company:", list(STOCK_CATEGORIES[category].keys()))
    ticker = STOCK_CATEGORIES[category][selected_company]
    
    st.markdown("---")
    
    # Investment amount with presets
    st.subheader("💰 Investment Amount")
    preset_amounts = [100, 500, 1000, 5000, 10000]
    
    col1, col2 = st.columns(2)
    with col1:
        for amount in preset_amounts[:3]:
            if st.button(f"${amount:,}", key=f"preset_{amount}"):
                st.session_state.investment_amount = amount
    with col2:
        for amount in preset_amounts[3:]:
            if st.button(f"${amount:,}", key=f"preset_{amount}"):
                st.session_state.investment_amount = amount
    
    investment_amount = st.number_input(
        "Or enter custom amount (USD):", 
        min_value=10, 
        max_value=100000, 
        value=st.session_state.get('investment_amount', 1000), 
        step=10
    )
    
    st.markdown("---")
    
    # Date selection with presets
    st.subheader("📅 Time Period")
    
    # Quick date presets
    date_presets = {
        "1 Year Ago": 365,
        "2 Years Ago": 730,
        "5 Years Ago": 1825,
        "10 Years Ago": 3650
    }
    
    selected_preset = st.selectbox("Quick Select:", ["Custom"] + list(date_presets.keys()))
    
    if selected_preset != "Custom":
        days_back = date_presets[selected_preset]
        default_start = datetime.now() - timedelta(days=days_back)
    else:
        default_start = datetime.now() - timedelta(days=365)
    
    start_date = st.date_input(
        "Start Date:", 
        value=default_start.date(),
        max_value=datetime.now().date() - timedelta(days=1)
    )
    
    end_date = st.date_input(
        "End Date:", 
        value=datetime.now().date(),
        max_value=datetime.now().date()
    )
    
    st.markdown("---")
    calculate_button = st.button("🚀 Calculate Returns!", type="primary", use_container_width=True)

# Cache function for better performance
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_stock_data(ticker, start, end):
    """Fetch stock data with error handling"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start, end=end)
        
        if data.empty:
            st.error(f"No data available for {ticker} in the selected period.")
            return None
            
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

def calculate_returns(data, investment_amount):
    """Calculate investment returns with additional metrics"""
    if data is None or len(data) == 0:
        return None
    
    start_price = data['Close'].iloc[0]
    end_price = data['Close'].iloc[-1]
    shares_bought = investment_amount / start_price
    final_value = shares_bought * end_price
    total_return = final_value - investment_amount
    return_percentage = (total_return / investment_amount) * 100
    
    # Additional metrics
    max_price = data['Close'].max()
    min_price = data['Close'].min()
    max_value = shares_bought * max_price
    min_value = shares_bought * min_price
    
    # Volatility (standard deviation of daily returns)
    daily_returns = data['Close'].pct_change().dropna()
    volatility = daily_returns.std() * np.sqrt(252) * 100  # Annualized volatility
    
    return {
        'start_price': start_price,
        'end_price': end_price,
        'shares_bought': shares_bought,
        'final_value': final_value,
        'total_return': total_return,
        'return_percentage': return_percentage,
        'max_value': max_value,
        'min_value': min_value,
        'max_price': max_price,
        'min_price': min_price,
        'volatility': volatility,
        'days_held': len(data)
    }

# Main calculation logic
if calculate_button:
    if start_date >= end_date:
        st.error("⚠️ Start date must be before end date!")
    else:
        with st.spinner("Calculating your returns... 🔄"):
            stock_data = get_stock_data(ticker, start_date, end_date)
            
            if stock_data is not None and len(stock_data) > 0:
                results = calculate_returns(stock_data, investment_amount)
                
                if results:
                    # Main metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("💰 Initial Investment", f"${investment_amount:,.2f}")
                    with col2:
                        st.metric("📈 Final Value", f"${results['final_value']:,.2f}",
                                delta=f"${results['total_return']:,.2f}")
                    with col3:
                        st.metric("📊 Total Return", f"{results['return_percentage']:.2f}%")
                    with col4:
                        st.metric("📅 Days Held", f"{results['days_held']}")
                    
                    # Additional metrics
                    col5, col6, col7, col8 = st.columns(4)
                    with col5:
                        st.metric("🔺 Peak Value", f"${results['max_value']:,.2f}")
                    with col6:
                        st.metric("🔻 Lowest Value", f"${results['min_value']:,.2f}")
                    with col7:
                        st.metric("📈 Highest Price", f"${results['max_price']:.2f}")
                    with col8:
                        st.metric("⚡ Volatility", f"{results['volatility']:.1f}%")
                    
                    # Result summary box
                    if results['total_return'] > 0:
                        st.markdown(f"""
                        <div class="profit-box">
                            <h3>🎉 Congratulations!</h3>
                            <p>If you had invested <strong>${investment_amount:,.2f}</strong> in {selected_company} on {start_date.strftime('%B %d, %Y')}, 
                            you would have <strong>${results['final_value']:,.2f}</strong> today!</p>
                            <p><strong>That's a profit of ${results['total_return']:,.2f} ({results['return_percentage']:.2f}%)</strong></p>
                            <p>You would have bought {results['shares_bought']:.2f} shares at ${results['start_price']:.2f} each.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="loss-box">
                            <h3>📉 Ouch!</h3>
                            <p>If you had invested <strong>${investment_amount:,.2f}</strong> in {selected_company} on {start_date.strftime('%B %d, %Y')}, 
                            you would have <strong>${results['final_value']:,.2f}</strong> today.</p>
                            <p><strong>That's a loss of ${abs(results['total_return']):,.2f} ({results['return_percentage']:.2f}%)</strong></p>
                            <p>You would have bought {results['shares_bought']:.2f} shares at ${results['start_price']:.2f} each.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Interactive chart
                    st.subheader(f"📈 {selected_company} Stock Price Chart")
                    
                    fig = go.Figure()
                    
                    # Main price line
                    fig.add_trace(go.Scatter(
                        x=stock_data.index,
                        y=stock_data['Close'],
                        mode='lines',
                        name=f'{selected_company} Price',
                        line=dict(color='#667eea', width=3),
                        hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: $%{y:.2f}<extra></extra>'
                    ))
                    
                    # Buy point
                    fig.add_trace(go.Scatter(
                        x=[stock_data.index[0]],
                        y=[results['start_price']],
                        mode='markers',
                        name='Buy Point',
                        marker=dict(color='green', size=20, symbol='triangle-up'),
                        hovertemplate='<b>Buy Date</b>: %{x}<br><b>Buy Price</b>: $%{y:.2f}<extra></extra>'
                    ))
                    
                    # Sell point
                    fig.add_trace(go.Scatter(
                        x=[stock_data.index[-1]],
                        y=[results['end_price']],
                        mode='markers',
                        name='Sell Point',
                        marker=dict(color='red', size=20, symbol='triangle-down'),
                        hovertemplate='<b>Sell Date</b>: %{x}<br><b>Sell Price</b>: $%{y:.2f}<extra></extra>'
                    ))
                    
                    # Highest and lowest points
                    max_idx = stock_data['Close'].idxmax()
                    min_idx = stock_data['Close'].idxmin()
                    
                    fig.add_trace(go.Scatter(
                        x=[max_idx],
                        y=[results['max_price']],
                        mode='markers',
                        name='Peak Price',
                        marker=dict(color='gold', size=15, symbol='star'),
                        hovertemplate='<b>Peak Date</b>: %{x}<br><b>Peak Price</b>: $%{y:.2f}<extra></extra>'
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=[min_idx],
                        y=[results['min_price']],
                        mode='markers',
                        name='Lowest Price',
                        marker=dict(color='purple', size=15, symbol='diamond'),
                        hovertemplate='<b>Lowest Date</b>: %{x}<br><b>Lowest Price</b>: $%{y:.2f}<extra></extra>'
                    ))
                    
                    fig.update_layout(
                        title=f"{selected_company} Stock Price: {start_date} to {end_date}",
                        xaxis_title="Date",
                        yaxis_title="Price (USD)",
                        template='plotly_white',
                        hovermode='x unified',
                        height=600
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Performance analysis
                    st.subheader("📊 Performance Analysis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="info-box">
                            <h4>📈 Investment Summary</h4>
                            <p><strong>Investment Period:</strong> {results['days_held']} days</p>
                            <p><strong>Annualized Return:</strong> {(results['return_percentage'] * 365 / results['days_held']):.2f}%</p>
                            <p><strong>Best Possible Return:</strong> ${results['max_value'] - investment_amount:,.2f}</p>
                            <p><strong>Worst Possible Loss:</strong> ${results['min_value'] - investment_amount:,.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        # Risk assessment
                        risk_level = "Low" if results['volatility'] < 20 else "Medium" if results['volatility'] < 40 else "High"
                        risk_color = "#28a745" if risk_level == "Low" else "#ffc107" if risk_level == "Medium" else "#dc3545"
                        
                        st.markdown(f"""
                        <div class="info-box">
                            <h4>⚡ Risk Assessment</h4>
                            <p><strong>Volatility:</strong> {results['volatility']:.1f}%</p>
                            <p><strong>Risk Level:</strong> <span style="color: {risk_color}; font-weight: bold;">{risk_level}</span></p>
                            <p><strong>Price Range:</strong> ${results['min_price']:.2f} - ${results['max_price']:.2f}</p>
                            <p><strong>Max Drawdown:</strong> {((results['min_value'] - results['max_value']) / results['max_value'] * 100):.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)

# Information section
st.markdown("---")
st.markdown("""
### How It Works 🤔

This tool uses real historical stock data to show you exactly what would have happened if you had invested in popular stocks at any point in the past.

**Features:**
- ✅ Real-time data from Yahoo Finance
- ✅ 40+ popular stocks across different sectors
- ✅ Detailed performance metrics and risk analysis
- ✅ Interactive charts with buy/sell points
- ✅ Volatility and drawdown analysis

**How to Use:**
1. 🎯 Select a stock category and company
2. 💰 Choose your investment amount
3. 📅 Pick your investment period
4. 🚀 Click "Calculate Returns" to see the results!

**Disclaimer:** Past performance does not guarantee future results. This tool is for educational purposes only and should not be considered as investment advice.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📊 Investment Backtesting Tool | Built with Streamlit & ❤️</p>
    <p><em>Data provided by Yahoo Finance</em></p>
</div>
""", unsafe_allow_html=True)
