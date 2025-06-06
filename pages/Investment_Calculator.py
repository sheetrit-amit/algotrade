import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="תיק השקעות אחורנית 💼",
    page_icon="💼",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .success-box {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .warning-box {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>💼 תיק השקעות אחורנית</h1>
    <p>גלה כמה היית יכול להרוויח אילו השקעת בעבר!</p>
</div>
""", unsafe_allow_html=True)

POPULAR_STOCKS = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Google': 'GOOGL',
    'Amazon': 'AMZN',
    'Tesla': 'TSLA',
    'Disney': 'DIS',
    'McDonald\'s': 'MCD',
    'Nike': 'NKE',
    'Coca-Cola': 'KO',
    'Netflix': 'NFLX'
}

with st.sidebar:
    st.header("🎯 בחר את ההשקעה שלך")
    selected_company = st.selectbox("בחר חברה:", list(POPULAR_STOCKS.keys()))
    ticker = POPULAR_STOCKS[selected_company]
    investment_amount = st.number_input("כמה כסף היית רוצה להשקיע? (בדולרים)", 
                                      min_value=10, max_value=10000, value=100, step=10)
    
    st.subheader("📅 בחר תקופה")
    start_date = st.date_input("תאריך התחלה:", 
                              value=datetime.now() - timedelta(days=365),
                              max_value=datetime.now() - timedelta(days=1))
    end_date = st.date_input("תאריך סיום:", 
                            value=datetime.now(),
                            max_value=datetime.now())
    
    calculate_button = st.button("🚀 חשב את הרווח!", type="primary")

@st.cache_data
def get_stock_data(ticker, start, end):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start, end=end)
        return data
    except Exception as e:
        st.error(f"שגיאה בהורדת נתונים: {e}")
        return None

def calculate_returns(data, investment_amount):
    if data is None or len(data) == 0:
        return None
    
    start_price = data['Close'].iloc[0]
    end_price = data['Close'].iloc[-1]
    shares_bought = investment_amount / start_price
    final_value = shares_bought * end_price
    total_return = final_value - investment_amount
    return_percentage = (total_return / investment_amount) * 100
    
    return {
        'start_price': start_price,
        'end_price': end_price,
        'shares_bought': shares_bought,
        'final_value': final_value,
        'total_return': total_return,
        'return_percentage': return_percentage
    }

if calculate_button:
    if start_date >= end_date:
        st.error("⚠️ תאריך ההתחלה חייב להיות לפני תאריך הסיום!")
    else:
        with st.spinner("מחשב את הרווח שלך... 🔄"):
            stock_data = get_stock_data(ticker, start_date, end_date)
            
            if stock_data is not None and len(stock_data) > 0:
                results = calculate_returns(stock_data, investment_amount)
                
                if results:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("💰 השקעה ראשונית", f"${investment_amount:,.2f}")
                    with col2:
                        st.metric("📈 ערך סופי", f"${results['final_value']:,.2f}",
                                delta=f"${results['total_return']:,.2f}")
                    with col3:
                        st.metric("📊 תשואה באחוזים", f"{results['return_percentage']:.2f}%")
                    
                    if results['total_return'] > 0:
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>🎉 כל הכבוד!</h3>
                            <p>אילו השקעת ${investment_amount:,.2f} ב-{selected_company} ב-{start_date.strftime('%d/%m/%Y')}, 
                            היום היית בעל ${results['final_value']:,.2f}!</p>
                            <p><strong>זה רווח של ${results['total_return']:,.2f}!</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="warning-box">
                            <h3>📉 אוי לא!</h3>
                            <p>אילו השקעת ${investment_amount:,.2f} ב-{selected_company} ב-{start_date.strftime('%d/%m/%Y')}, 
                            היום היית בעל ${results['final_value']:,.2f}</p>
                            <p><strong>זה הפסד של ${abs(results['total_return']):,.2f}</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.subheader(f"📈 גרף מחיר {selected_company}")
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=stock_data.index,
                        y=stock_data['Close'],
                        mode='lines',
                        name=f'{selected_company} מחיר',
                        line=dict(color='#667eea', width=3)
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=[stock_data.index[0]],
                        y=[results['start_price']],
                        mode='markers',
                        name='נקודת רכישה',
                        marker=dict(color='green', size=15, symbol='triangle-up')
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=[stock_data.index[-1]],
                        y=[results['end_price']],
                        mode='markers',
                        name='נקודת מכירה',
                        marker=dict(color='red', size=15, symbol='triangle-down')
                    ))
                    
                    fig.update_layout(
                        title=f"מחיר {selected_company} מ-{start_date} עד {end_date}",
                        xaxis_title="תאריך",
                        yaxis_title="מחיר ($)",
                        template='plotly_white'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("""
### איך זה עובד? 🤔
1. בחר חברה מתוך הרשימה
2. הזן סכום השקעה  
3. בחר תאריכים
4. לחץ חשב ותראה התוצאות!
""")
