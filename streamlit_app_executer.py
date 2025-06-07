import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AlgoTrade Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
        height: 100%;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    .feature-title {
        color: #2c3e50;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .feature-description {
        color: #5a6c7d;
        line-height: 1.6;
    }
    .stats-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    .stat-item {
        text-align: center;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        display: block;
    }
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .cta-section {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 3rem 0;
    }
    .section-header {
        color: #2c3e50;
        font-size: 2.2rem;
        font-weight: 600;
        text-align: center;
        margin: 3rem 0 2rem 0;
        border-bottom: 3px solid #667eea;
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">📈 AlgoTrade Platform</div>
    <div class="hero-subtitle">Professional Investment Analysis & Backtesting Tools</div>
    <p>Empowering traders and investors with data-driven insights and advanced analytical tools</p>
</div>
""", unsafe_allow_html=True)

# Navigation hint
st.markdown("### 🚀 Quick Start")
st.info("👈 **Choose a tool from the sidebar to get started!** Each tool provides powerful analytics for different aspects of investment analysis.")

# Platform Features
st.markdown('<h2 class="section-header">Platform Features</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Investment Backtesting</div>
        <div class="feature-description">
            Analyze historical performance of stocks and ETFs with comprehensive metrics including volatility, 
            maximum drawdown, and risk assessment. Test your investment strategies with real market data.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💹</div>
        <div class="feature-title">Portfolio Analysis</div>
        <div class="feature-description">
            Advanced portfolio performance tracking and optimization tools. Analyze risk-adjusted returns, 
            diversification metrics, and compare your portfolio against market benchmarks.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔬</div>
        <div class="feature-title">Risk Analytics</div>
        <div class="feature-description">
            Comprehensive risk analysis including Value at Risk (VaR), volatility modeling, and stress testing. 
            Understand your exposure and optimize your risk-return profile.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Platform Statistics
st.markdown('<h2 class="section-header">Platform Statistics</h2>', unsafe_allow_html=True)

# Create some sample market data visualization
dates = np.arange(30)
market_trend = 100 + np.cumsum(np.random.randn(30) * 0.5)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-item">
        <span class="stat-number">40+</span>
        <span class="stat-label">Stocks Available</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-item">
        <span class="stat-number">15+</span>
        <span class="stat-label">Years of Data</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-item">
        <span class="stat-number">24/7</span>
        <span class="stat-label">Real-time Updates</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-item">
        <span class="stat-number">100%</span>
        <span class="stat-label">Free to Use</span>
    </div>
    """, unsafe_allow_html=True)

# Sample Chart
st.markdown('<h2 class="section-header">Market Overview</h2>', unsafe_allow_html=True)

# Create a sample market overview chart
fig = go.Figure()

# Sample data for demonstration
sample_dates = [f"2024-0{i+1}-01" for i in range(12)]
sample_values = [100 + i*2 + np.random.randn()*5 for i in range(12)]

fig.add_trace(go.Scatter(
    x=sample_dates,
    y=sample_values,
    mode='lines+markers',
    name='Market Index',
    line=dict(color='#667eea', width=3),
    marker=dict(size=6)
))

fig.update_layout(
    title="Sample Market Performance Overview",
    xaxis_title="Time Period",
    yaxis_title="Index Value",
    template='plotly_white',
    height=400,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Available Tools Section
st.markdown('<h2 class="section-header">Available Tools</h2>', unsafe_allow_html=True)

tools_col1, tools_col2 = st.columns(2)

with tools_col1:
    with st.expander("📊 Investment Backtesting Tool", expanded=True):
        st.write("""
        **What it does:**
        - Historical performance analysis of 40+ stocks and ETFs
        - Comprehensive risk metrics and volatility analysis
        - Interactive charts with buy/sell point visualization
        - Performance comparison across different time periods
        
        **Best for:**
        - Evaluating past investment decisions
        - Understanding risk-return profiles
        - Educational purposes and strategy validation
        """)

with tools_col2:
    with st.expander("🔧 More Tools Coming Soon", expanded=False):
        st.write("""
        **Planned Features:**
        - Real-time portfolio tracker
        - Options strategy analyzer
        - Cryptocurrency analysis tools
        - Economic indicator dashboard
        - Automated trading signal generator
        
        **Stay tuned for updates!**
        """)

# Call to Action
st.markdown("""
<div class="cta-section">
    <h2>Ready to Start Analyzing?</h2>
    <p>Join thousands of traders and investors using AlgoTrade Platform for smarter investment decisions</p>
    <p><strong>👈 Select a tool from the sidebar to begin your analysis!</strong></p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    **About AlgoTrade**
    - Professional-grade tools
    - Real market data
    - Educational focus
    """)

with footer_col2:
    st.markdown("""
    **Data Sources**
    - Yahoo Finance API
    - Real-time market feeds
    - Historical databases
    """)

with footer_col3:
    st.markdown("""
    **Disclaimer**
    - Educational purposes only
    - Not financial advice
    - Past performance ≠ future results
    """)

st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem; margin-top: 2rem; border-top: 1px solid #ecf0f1;">
    <p><strong>AlgoTrade Platform</strong> | Built with ❤️ using Streamlit</p>
    <p>© 2025 AlgoTrade. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
