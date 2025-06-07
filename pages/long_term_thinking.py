import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Long-Term Investment Perspectives",
    page_icon="📈",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .item-card {
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f8f9fa;
        border-left: 5px solid #4CAF50;
    }
    .result-box {
        background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
    }
    .stSelectbox > div > div {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("📈 Long-Term Investment Perspectives")
st.markdown("""
### What if you had invested instead of buying that item?

See how much your money could have grown if you invested in the stock market instead of making certain purchases.
""")

# Available items with their 2010 prices (in USD)
ITEMS = {
    "iPhone 4 (2010)": {"price": 599, "emoji": "📱"},
    "Gaming Console (PS3/Xbox 360)": {"price": 299, "emoji": "🎮"},
    "Designer Handbag": {"price": 1200, "emoji": "👜"},
    "Bicycle": {"price": 500, "emoji": "🚴"},
    "Laptop": {"price": 1000, "emoji": "💻"}
}

# Popular stocks to invest in
STOCKS = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "GOOGL": "Alphabet (Google)",
    "META": "Meta (Facebook)",
    "TSLA": "Tesla",
    "NVDA": "NVIDIA"
}

# Sidebar for user input
with st.sidebar:
    st.header("Investment Calculator")
    selected_item = st.selectbox(
        "What would you like to buy?",
        options=list(ITEMS.keys()),
        format_func=lambda x: f"{ITEMS[x]['emoji']} {x} (${ITEMS[x]['price']})"
    )
    
    selected_stock = st.selectbox(
        "Which stock would you invest in?",
        options=list(STOCKS.keys()),
        format_func=lambda x: f"{x} - {STOCKS[x]}"
    )
    
    investment_year = st.slider(
        "When would you have made this purchase?",
        min_value=2010,
        max_value=2023,
        value=2010,
        step=1
    )

# Get the selected item's price
item_price = ITEMS[selected_item]["price"]

# Calculate date range for stock data
end_date = datetime.now()
start_date = datetime(investment_year, 1, 1)

# Show loading state
with st.spinner(f'Fetching {selected_stock} stock data...'):
    try:
        # Get stock data
        stock_data = yf.download(selected_stock, start=start_date, end=end_date)
        
        if stock_data.empty:
            st.error("No data found for the selected stock and date range.")
            st.stop()
            
        # Calculate investment growth
        initial_price = float(stock_data['Close'].iloc[0])
        current_price = float(stock_data['Close'].iloc[-1])
        shares_bought = item_price / initial_price
        current_value = shares_bought * current_price
        profit = current_value - item_price
        
        # Format numbers for display
        formatted_price = '${:,.2f}'.format(item_price)
        formatted_value = '${:,.2f}'.format(current_value)
        
        # Calculate growth over time
        stock_data['Investment_Value'] = (item_price / initial_price) * stock_data['Close']
        
        # Create the plot
        fig = px.line(
            stock_data,
            x=stock_data.index,
            y='Investment_Value',
            title=f'Growth of ${item_price} Invested in {selected_stock} in {investment_year}',
            labels={'Investment_Value': 'Investment Value ($)', 'index': 'Date'}
        )
        
        # Add horizontal line for initial investment
        fig.add_hline(
            y=item_price,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Initial Investment: ${item_price:,.2f}"
        )
        
        # Update layout
        fig.update_layout(
            hovermode='x unified',
            showlegend=False,
            xaxis_title='',
            yaxis_title='Investment Value ($)',
            template='plotly_white'
        )
        
        # Display results
        st.plotly_chart(fig, use_container_width=True)
        
        # Show summary with formatted values
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%); 
                    color: white; 
                    padding: 20px; 
                    border-radius: 10px; 
                    margin: 20px 0; 
                    text-align: center;'>
            <p>If you had invested <strong>{formatted_price}</strong> in {selected_stock} in {investment_year} instead of buying {selected_item.lower()}:</p>
            <div style='font-size: 3.5rem; 
                        font-weight: 700; 
                        color: #2e7d32; 
                        text-align: center; 
                        margin: 20px 0;'>
                {formatted_value} today
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Educational note
st.markdown("""
### 💡 Did You Know?
- The stock market has historically returned about 7% annually after inflation
- The longer you stay invested, the more your money can grow through compounding
- Past performance doesn't guarantee future results, but history shows that markets tend to go up over time

*This is for educational purposes only and not financial advice. Always do your own research before investing.*
""")