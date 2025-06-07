import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Investment Backtesting Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        padding: 3rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 300;
    }
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    .profit-box {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 6px 24px rgba(39, 174, 96, 0.2);
    }
    .loss-box {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 6px 24px rgba(231, 76, 60, 0.2);
    }
    .info-box {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        padding: 1.8rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 6px 24px rgba(52, 73, 94, 0.2);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    .section-header {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    .sidebar-header {
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #bdc3c7;
    }
    .disclaimer {
        background: #f8f9fa;
        border-left: 4px solid #3498db;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        font-size: 0.9rem;
        color: #5a5a5a;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>Investment Backtesting Tool</h1>
    <p>Analyze historical investment performance with real market data</p>
</div>
""", unsafe_allow_html=True)

# Expanded stock selection with categories
STOCK_CATEGORIES = {
    'Technology': {
        'Apple Inc.': 'AAPL',
        'Microsoft Corporation': 'MSFT',
        'Alphabet Inc.': 'GOOGL',
        'Amazon.com Inc.': 'AMZN',
        'Meta Platforms Inc.': 'META',
        'Netflix Inc.': 'NFLX',
        'Adobe Inc.': 'ADBE',
        'Salesforce Inc.': 'CRM',
        'NVIDIA Corporation': 'NVDA',
        'Intel Corporation': 'INTC'
    },
    'Consumer & Retail': {
        'Tesla Inc.': 'TSLA',
        'The Walt Disney Company': 'DIS',
        'McDonald\'s Corporation': 'MCD',
        'Nike Inc.': 'NKE',
        'The Coca-Cola Company': 'KO',
        'Starbucks Corporation': 'SBUX',
        'The Home Depot Inc.': 'HD',
        'Walmart Inc.': 'WMT',
        'Procter & Gamble Co.': 'PG',
        'Johnson & Johnson': 'JNJ'
    },
    'Financial Services': {
        'Berkshire Hathaway Inc.': 'BRK-B',
        'JPMorgan Chase & Co.': 'JPM',
        'Bank of America Corp.': 'BAC',
        'Wells Fargo & Company': 'WFC',
        'The Goldman Sachs Group': 'GS',
        'American Express Company': 'AXP',
        'PayPal Holdings Inc.': 'PYPL',
        'Visa Inc.': 'V',
        'Mastercard Incorporated': 'MA'
    },
    'Cryptocurrency ETFs': {
        'ProShares Bitcoin Strategy ETF': 'BITO',
        'Grayscale Ethereum Trust': 'ETHE'
    }
}

# Sidebar configuration
with st.sidebar:
    st.markdown('<div class="sidebar-header">Investment Configuration</div>', unsafe_allow_html=True)
    
    # Category selection
    category = st.selectbox("Select Sector:", list(STOCK_CATEGORIES.keys()))
    
    # Stock selection within category
    selected_company = st.selectbox("Choose Company:", list(STOCK_CATEGORIES[category].keys()))
    ticker = STOCK_CATEGORIES[category][selected_company]
    
    st.markdown("---")
    
    # Investment amount with presets
    st.markdown('<div class="sidebar-header">Investment Amount</div>', unsafe_allow_html=True)
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
        "Custom amount (USD):", 
        min_value=10, 
        max_value=100000, 
        value=st.session_state.get('investment_amount', 1000), 
        step=10
    )
    
    st.markdown("---")
    
    # Date selection with presets
    st.markdown('<div class="sidebar-header">Investment Period</div>', unsafe_allow_html=True)
    
    # Quick date presets
    date_presets = {
        "1 Year": 365,
        "2 Years": 730,
        "5 Years": 1825,
        "10 Years": 3650
    }
    
    selected_preset = st.selectbox("Quick Select:", ["Custom Period"] + list(date_presets.keys()))
    
    if selected_preset != "Custom Period":
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
    calculate_button = st.button("Calculate Returns", type="primary", use_container_width=True)

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
        st.error("Start date must be before end date.")
    else:
        with st.spinner("Analyzing investment performance..."):
            stock_data = get_stock_data(ticker, start_date, end_date)
            
            if stock_data is not None and len(stock_data) > 0:
                results = calculate_returns(stock_data, investment_amount)
                
                if results:
                    # Main metrics
                    st.markdown('<h2 class="section-header">Investment Summary</h2>', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Initial Investment", f"${investment_amount:,.2f}")
                    with col2:
                        st.metric("Final Value", f"${results['final_value']:,.2f}",
                                delta=f"${results['total_return']:,.2f}")
                    with col3:
                        st.metric("Total Return", f"{results['return_percentage']:.2f}%")
                    with col4:
                        st.metric("Investment Period", f"{results['days_held']} days")
                    
                    # Additional metrics
                    col5, col6, col7, col8 = st.columns(4)
                    with col5:
                        st.metric("Peak Portfolio Value", f"${results['max_value']:,.2f}")
                    with col6:
                        st.metric("Lowest Portfolio Value", f"${results['min_value']:,.2f}")
                    with col7:
                        st.metric("Highest Share Price", f"${results['max_price']:.2f}")
                    with col8:
                        st.metric("Annual Volatility", f"{results['volatility']:.1f}%")
                    
                    # Result summary box
                    if results['total_return'] > 0:
                        st.markdown(f"""
                        <div class="profit-box">
                            <h3>Investment Result: Profitable</h3>
                            <p>Your investment of <strong>${investment_amount:,.2f}</strong> in {selected_company} 
                            from {start_date.strftime('%B %d, %Y')} would be worth <strong>${results['final_value']:,.2f}</strong> today.</p>
                            <p><strong>Net Profit: ${results['total_return']:,.2f} ({results['return_percentage']:.2f}% total return)</strong></p>
                            <p>This represents {results['shares_bought']:.2f} shares purchased at ${results['start_price']:.2f} per share.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="loss-box">
                            <h3>Investment Result: Loss</h3>
                            <p>Your investment of <strong>${investment_amount:,.2f}</strong> in {selected_company} 
                            from {start_date.strftime('%B %d, %Y')} would be worth <strong>${results['final_value']:,.2f}</strong> today.</p>
                            <p><strong>Net Loss: ${abs(results['total_return']):,.2f} ({results['return_percentage']:.2f}% total return)</strong></p>
                            <p>This represents {results['shares_bought']:.2f} shares purchased at ${results['start_price']:.2f} per share.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Interactive chart
                    st.markdown('<h2 class="section-header">Price Performance Chart</h2>', unsafe_allow_html=True)
                    
                    fig = go.Figure()
                    
                    # Main price line
                    fig.add_trace(go.Scatter(
                        x=stock_data.index,
                        y=stock_data['Close'],
                        mode='lines',
                        name=f'{selected_company}',
                        line=dict(color='#3498db', width=2.5),
                        hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: $%{y:.2f}<extra></extra>'
                    ))
                    
                    # Buy point
                    fig.add_trace(go.Scatter(
                        x=[stock_data.index[0]],
                        y=[results['start_price']],
                        mode='markers',
                        name='Purchase Date',
                        marker=dict(color='#27ae60', size=12, symbol='triangle-up'),
                        hovertemplate='<b>Purchase Date</b>: %{x}<br><b>Purchase Price</b>: $%{y:.2f}<extra></extra>'
                    ))
                    
                    # Sell point
                    fig.add_trace(go.Scatter(
                        x=[stock_data.index[-1]],
                        y=[results['end_price']],
                        mode='markers',
                        name='End Date',
                        marker=dict(color='#e74c3c', size=12, symbol='triangle-down'),
                        hovertemplate='<b>End Date</b>: %{x}<br><b>End Price</b>: $%{y:.2f}<extra></extra>'
                    ))
                    
                    # Highest and lowest points
                    max_idx = stock_data['Close'].idxmax()
                    min_idx = stock_data['Close'].idxmin()
                    
                    fig.add_trace(go.Scatter(
                        x=[max_idx],
                        y=[results['max_price']],
                        mode='markers',
                        name='Peak Price',
                        marker=dict(color='#f39c12', size=10, symbol='star'),
                        hovertemplate='<b>Peak Date</b>: %{x}<br><b>Peak Price</b>: $%{y:.2f}<extra></extra>'
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=[min_idx],
                        y=[results['min_price']],
                        mode='markers',
                        name='Lowest Price',
                        marker=dict(color='#9b59b6', size=10, symbol='diamond'),
                        hovertemplate='<b>Lowest Date</b>: %{x}<br><b>Lowest Price</b>: $%{y:.2f}<extra></extra>'
                    ))
                    
                    fig.update_layout(
                        title=f"{selected_company} Stock Performance: {start_date} to {end_date}",
                        xaxis_title="Date",
                        yaxis_title="Price (USD)",
                        template='plotly_white',
                        hovermode='x unified',
                        height=500,
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Performance analysis
                    st.markdown('<h2 class="section-header">Detailed Analysis</h2>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        annualized_return = (results['return_percentage'] * 365 / results['days_held']) if results['days_held'] > 0 else 0
                        best_return = results['max_value'] - investment_amount
                        worst_return = results['min_value'] - investment_amount
                        
                        st.markdown(f"""
                        <div class="info-box">
                            <h4>Performance Metrics</h4>
                            <p><strong>Investment Duration:</strong> {results['days_held']} days ({results['days_held']/365:.1f} years)</p>
                            <p><strong>Annualized Return:</strong> {annualized_return:.2f}%</p>
                            <p><strong>Best Possible Outcome:</strong> ${best_return:,.2f} profit</p>
                            <p><strong>Worst Possible Outcome:</strong> ${worst_return:,.2f} loss</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        # Risk assessment
                        if results['volatility'] < 20:
                            risk_level, risk_color = "Low", "#27ae60"
                        elif results['volatility'] < 40:
                            risk_level, risk_color = "Medium", "#f39c12"
                        else:
                            risk_level, risk_color = "High", "#e74c3c"
                        
                        max_drawdown = ((results['min_value'] - results['max_value']) / results['max_value'] * 100) if results['max_value'] > 0 else 0
                        price_range_pct = ((results['max_price'] - results['min_price']) / results['min_price'] * 100) if results['min_price'] > 0 else 0
                        
                        st.markdown(f"""
                        <div class="info-box">
                            <h4>Risk Assessment</h4>
                            <p><strong>Volatility Level:</strong> {results['volatility']:.1f}% annually</p>
                            <p><strong>Risk Category:</strong> <span style="color: {risk_color}; font-weight: bold;">{risk_level}</span></p>
                            <p><strong>Price Range:</strong> ${results['min_price']:.2f} - ${results['max_price']:.2f} ({price_range_pct:.1f}%)</p>
                            <p><strong>Maximum Drawdown:</strong> {max_drawdown:.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)

# Information section
st.markdown('<h2 class="section-header">How This Tool Works</h2>', unsafe_allow_html=True)

st.markdown("""
This investment backtesting tool provides historical analysis of stock performance using real market data from Yahoo Finance. 
It shows exactly what would have happened if you had invested a specific amount in a chosen stock during any historical period.

**Key Features:**
- Real-time historical data from major stock exchanges
- Analysis of 40+ popular stocks across different sectors
- Comprehensive risk and performance metrics
- Interactive charts showing key price points
- Volatility analysis and maximum drawdown calculations

**How to Use:**
1. **Select a Sector:** Choose from Technology, Consumer & Retail, Financial Services, or Cryptocurrency ETFs
2. **Pick a Company:** Select from well-known companies in your chosen sector
3. **Set Investment Amount:** Use preset amounts or enter a custom value
4. **Choose Time Period:** Select from preset periods or specify custom dates
5. **Analyze Results:** Review the comprehensive performance analysis and interactive charts

**Understanding the Metrics:**
- **Total Return:** The percentage gain or loss on your investment
- **Volatility:** A measure of price fluctuation (higher = more risky)
- **Maximum Drawdown:** The largest peak-to-trough decline during the period
- **Annualized Return:** Your return converted to a yearly percentage
""")

st.markdown("""
<div class="disclaimer">
<strong>Important Disclaimer:</strong> This tool is designed for educational and research purposes only. 
Past performance does not guarantee future results. All investments carry risk, including the potential loss of principal. 
This analysis should not be considered as personalized investment advice. Please consult with a qualified financial advisor 
before making investment decisions.
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 1rem; font-size: 0.9rem;">
    <p><strong>Investment Backtesting Tool</strong> | Built with Streamlit</p>
    <p>Market data provided by Yahoo Finance</p>
</div>
""", unsafe_allow_html=True)
