import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AlgoTrade Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        padding: 2.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 400;
    }
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    .tool-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        height: 100%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .tool-title {
        color: #2c3e50;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .section-header {
        color: #2c3e50;
        font-size: 1.8rem;
        font-weight: 500;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>AlgoTrade Platform</h1>
    <p>Investment analysis and backtesting tools</p>
</div>
""", unsafe_allow_html=True)

# Quick navigation
st.info("Choose a tool from the sidebar to get started with your analysis.")

# Available Tools
st.markdown('<h2 class="section-header">Available Tools</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">Investment Backtesting Tool</div>
        <p>Analyze historical stock performance with real market data. Features include:</p>
        <ul>
            <li>40+ stocks across different sectors</li>
            <li>Historical performance analysis</li>
            <li>Risk metrics and volatility analysis</li>
            <li>Interactive charts and visualizations</li>
        </ul>
        <p><strong>Best for:</strong> Understanding how past investments would have performed</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">More Tools</div>
        <p>Additional analysis tools and features:</p>
        <ul>
            <li>Portfolio analysis (coming soon)</li>
            <li>Risk assessment tools</li>
            <li>Market data visualization</li>
            <li>Custom analysis features</li>
        </ul>
        <p><strong>Note:</strong> This platform is for educational purposes</p>
    </div>
    """, unsafe_allow_html=True)

# How to Use
st.markdown('<h2 class="section-header">How to Use</h2>', unsafe_allow_html=True)

st.markdown("""
1. **Select a tool** from the sidebar menu
2. **Choose your parameters** (stock, investment amount, time period)
3. **Run the analysis** to see detailed results
4. **Review the metrics** and interactive charts

The platform uses real market data from Yahoo Finance to provide accurate historical analysis.
""")

# Sample visualization
st.markdown('<h2 class="section-header">Sample Analysis</h2>', unsafe_allow_html=True)

# Create a simple sample chart
dates = np.arange(30)
prices = 100 + np.cumsum(np.random.randn(30) * 0.8)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=prices,
    mode='lines',
    name='Sample Stock Price',
    line=dict(color='#3498db', width=2)
))

fig.update_layout(
    title="Example: Stock Price Movement Over Time",
    xaxis_title="Days",
    yaxis_title="Price ($)",
    template='plotly_white',
    height=300
)

st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**Disclaimer:** This platform is designed for educational purposes. Past performance does not guarantee future results. 
Not intended as financial advice.

**Data Source:** Yahoo Finance API | **Built with:** Streamlit
""")
