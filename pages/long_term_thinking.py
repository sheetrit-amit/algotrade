import streamlit as st

st.set_page_config(page_title="Long-Term Thinking", layout="centered")

st.title("🧠 Long-Term Thinking")

st.markdown("""
In investing, patience is key. Compounding works best when you give your
investments many years to grow. Use this page as a reminder to stay the
course and focus on your long-term goals.
""")

st.markdown("---")

years = st.slider("Select an investment horizon (years)", 1, 50, 20)
rate = st.slider("Expected annual return (%)", 1.0, 15.0, 7.0)
initial = st.number_input("Initial investment ($)", 100.0, 1000000.0, 1000.0, step=100.0)

future_value = initial * (1 + rate / 100) ** years
st.write(f"After {years} years you could have around $ {future_value:,.2f}.")
