import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AlgoTrade Learning Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple CSS for kid-friendly design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    .info-box {
        background: #f8f9fa;
        color: #212121;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .fun-fact {
        background: linear-gradient(135deg, #FF9800 0%, #FF5722 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .section-header {
        color: #2196F3;
        font-size: 1.8rem;
        font-weight: 500;
        margin: 2rem 0 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📈 AlgoTrade Learning Platform</h1>
    <p>Learn about stocks and investments in a fun way!</p>
</div>
""", unsafe_allow_html=True)

# Welcome message
st.markdown("""
<div class="info-box">
    <h3>🎉 Welcome Young Investors!</h3>
    <p>This platform will help you learn how the stock market works and how people make money by investing in companies. 
    You can pretend to invest money and see what would have happened in the past!</p>
</div>
""", unsafe_allow_html=True)

# What you can learn
st.markdown('<h2 class="section-header">🎓 What Will You Learn?</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📊 How Stocks Work
    - What are stocks and why do people buy them?
    - How do stock prices go up and down?
    - Which companies can you invest in?
    
    ### 💰 Making Smart Choices
    - How much money could you have made?
    - What happens when you invest for a long time?
    - Why some investments are risky and others are safe
    """)

with col2:
    st.markdown("""
    ### 📈 Reading Charts
    - How to read colorful charts and graphs
    - Understanding when prices go up or down
    - Finding the best and worst times to invest
    
    ### 🧮 Cool Math
    - Calculate profits and losses
    - Learn about percentages in real life
    - See how money can grow over time
    """)

# Fun fact
st.markdown("""
<div class="fun-fact">
    <h3>🤔 Did You Know?</h3>
    <p>If you had invested $100 in Apple stock 10 years ago, you could have over $1,000 today! 
    That's like turning one toy into ten toys!</p>
</div>
""", unsafe_allow_html=True)

# How to use
st.markdown('<h2 class="section-header">🚀 How to Get Started</h2>', unsafe_allow_html=True)

st.markdown("""
1. **👈 Click on a tool** in the sidebar (the menu on the left)
2. **🏢 Pick a company** you know (like Apple, Disney, or McDonald's)
3. **💵 Choose how much money** you want to pretend to invest
4. **📅 Pick dates** from the past to see what would have happened
5. **✨ Click the button** to see the magic happen!

Don't worry - this is all pretend money, so you can't lose anything real!
""")

# Simple example chart
st.markdown('<h2 class="section-header">📊 Example: How Stock Prices Change</h2>', unsafe_allow_html=True)

# Create a simple, colorful example
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
prices = [10, 12, 11, 15, 13]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=days,
    y=prices,
    mode='lines+markers',
    name='Stock Price',
    line=dict(color='#4CAF50', width=4),
    marker=dict(size=10, color='#FF9800')
))

fig.update_layout(
    title="📈 A Stock Price During One Week",
    xaxis_title="Days of the Week",
    yaxis_title="Price ($)",
    template='plotly_white',
    height=400,
    font=dict(size=14)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("See how the price goes up and down? That's normal for stocks!")

# Learning goals
st.markdown('<h2 class="section-header">🎯 What You\'ll Discover</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🏆 Best Investments**
    - Which companies made the most money
    - When was the best time to buy
    """)

with col2:
    st.markdown("""
    **⚠️ Risky vs Safe**
    - Some stocks jump around a lot
    - Others are more steady and calm
    """)

with col3:
    st.markdown("""
    **📚 Real Math**
    - Use percentages like grown-ups
    - Calculate profits like a business person
    """)

# Footer
st.markdown("---")
st.markdown("""
**Remember:** This is for learning only! Always ask a grown-up before making real money decisions.

**Cool Fact:** We use real information from the stock market to make this educational and accurate!

Made with ❤️ for young learners | Data from Yahoo Finance
""")
